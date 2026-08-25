param(
    [Parameter(Mandatory = $true)]
    [string]$SourceDirectory,

    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory
)

$ErrorActionPreference = "Stop"

$sourceRoot = (Resolve-Path -LiteralPath $SourceDirectory).Path
$outputRoot = (Resolve-Path -LiteralPath $OutputDirectory).Path
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$casualBase = Join-Path $projectRoot "game\mod_assets\char_sprites\himeko\neutral.png"
$uniformBase = Join-Path $projectRoot "game\mod_assets\char_sprites\himeko\neut_uniform.png"

Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Runtime.InteropServices;

public static class HimekoSpriteProcessor
{
    private const int Width = 1023;
    private const int Height = 1537;
    private const double FaceCenterX = 510.0;
    private const double FaceCenterY = 330.0;
    private const double FaceRadiusX = 185.0;
    private const double FaceRadiusY = 180.0;
    private const double SolidFaceRadius = 0.72;

    private sealed class Pixels
    {
        public readonly byte[] Bgra;
        public readonly double[] Edge;

        public Pixels(byte[] bgra, double[] edge)
        {
            Bgra = bgra;
            Edge = edge;
        }
    }

    private struct Registration
    {
        public double SampleScale;
        public int SampleDx;
        public int SampleDy;
        public double Score;
    }

    public static void CopyBase(string source, string destination)
    {
        ValidateCanvas(source);
        // Keep the two hand-authored source sprites byte-for-byte intact. GDI+
        // re-encoding can alter metadata on an otherwise identical PNG.
        File.Copy(source, destination, true);
    }

    public static void MakeTransparentFace(string destination)
    {
        using (var output = new Bitmap(Width, Height, PixelFormat.Format32bppArgb))
            output.Save(destination, ImageFormat.Png);
    }

    public static string MakeExpressionFace(
        string generated,
        string alphaReference,
        string secondaryAlphaReference,
        string destination)
    {
        ValidateCanvas(generated);
        ValidateCanvas(alphaReference);
        ValidateCanvas(secondaryAlphaReference);

        using (var inputBitmap = LoadArgb(generated))
        using (var referenceBitmap = LoadArgb(alphaReference))
        using (var secondaryReferenceBitmap = LoadArgb(secondaryAlphaReference))
        {
            Pixels input = ReadPixels(inputBitmap);
            Pixels reference = ReadPixels(referenceBitmap);
            Pixels secondaryReference = ReadPixels(secondaryReferenceBitmap);
            Registration registration = FindRegistration(reference, input);
            byte[] output = new byte[Width * Height * 4];

            for (int y = 0; y < Height; y++)
            {
                for (int x = 0; x < Width; x++)
                {
                    double normalizedX = (x - FaceCenterX) / FaceRadiusX;
                    double normalizedY = (y - FaceCenterY) / FaceRadiusY;
                    double distance = Math.Sqrt(
                        normalizedX * normalizedX + normalizedY * normalizedY);
                    if (distance >= 1.0)
                        continue;

                    double feather = distance <= SolidFaceRadius
                        ? 1.0
                        : (1.0 - distance) / (1.0 - SolidFaceRadius);
                    // Smoothstep avoids a visible elliptical collar when the
                    // generated rendering differs slightly from the original.
                    feather = feather * feather * (3.0 - 2.0 * feather);

                    int destinationIndex = (y * Width + x) * 4;
                    // The two hand-authored outfits differ by roughly one
                    // silhouette pixel around the head. Their alpha
                    // intersection prevents a shared face from expanding
                    // either outfit when Ren'Py composites it.
                    int referenceAlpha = Math.Min(
                        reference.Bgra[destinationIndex + 3],
                        secondaryReference.Bgra[destinationIndex + 3]);
                    int alpha = (int)Math.Round(referenceAlpha * feather);
                    if (alpha <= 0)
                        continue;

                    double sourceX = FaceCenterX
                        + (x - FaceCenterX) * registration.SampleScale
                        + registration.SampleDx;
                    double sourceY = FaceCenterY
                        + (y - FaceCenterY) * registration.SampleScale
                        + registration.SampleDy;
                    SampleBilinear(input.Bgra, sourceX, sourceY, output, destinationIndex);
                    output[destinationIndex + 3] = (byte)alpha;
                }
            }

            WritePixels(output, destination);
            return String.Format(
                "{0}: install shift ({1:+0;-0;0}, {2:+0;-0;0}) px, sample scale {3:0.000}, NCC {4:0.000}",
                Path.GetFileName(generated),
                -registration.SampleDx,
                -registration.SampleDy,
                registration.SampleScale,
                registration.Score);
        }
    }

    public static void RemoveCheckerboard(string generated, string destination)
    {
        ValidateCanvas(generated);

        using (var inputBitmap = LoadArgb(generated))
        {
            Pixels input = ReadPixels(inputBitmap);
            byte[] output = new byte[Width * Height * 4];
            bool[] background = new bool[Width * Height];
            bool[] visited = new bool[Width * Height];
            var queue = new Queue<int>();
            var component = new List<int>();

            for (int start = 0; start < Width * Height; start++)
            {
                if (visited[start])
                    continue;

                if (!IsBackgroundLike(input.Bgra, start))
                {
                    visited[start] = true;
                    continue;
                }

                component.Clear();
                queue.Enqueue(start);
                visited[start] = true;
                bool touchesCanvas = false;
                long minimumSum = 0;
                long chromaSum = 0;

                while (queue.Count > 0)
                {
                    int index = queue.Dequeue();
                    component.Add(index);
                    int x = index % Width;
                    int y = index / Width;
                    int byteIndex = index * 4;
                    int blue = input.Bgra[byteIndex];
                    int green = input.Bgra[byteIndex + 1];
                    int red = input.Bgra[byteIndex + 2];
                    int maximum = Math.Max(red, Math.Max(green, blue));
                    int minimum = Math.Min(red, Math.Min(green, blue));
                    minimumSum += minimum;
                    chromaSum += maximum - minimum;

                    if (x == 0 || y == 0 || x == Width - 1 || y == Height - 1)
                        touchesCanvas = true;

                    EnqueueBackground(x - 1, y, input.Bgra, visited, queue);
                    EnqueueBackground(x + 1, y, input.Bgra, visited, queue);
                    EnqueueBackground(x, y - 1, input.Bgra, visited, queue);
                    EnqueueBackground(x, y + 1, input.Bgra, visited, queue);
                }

                double averageMinimum = minimumSum / (double)component.Count;
                double averageChroma = chromaSum / (double)component.Count;
                bool isChecker = touchesCanvas ||
                    (component.Count >= 4 && averageMinimum >= 240.0 && averageChroma <= 2.2);
                if (isChecker)
                {
                    foreach (int index in component)
                        background[index] = true;
                }
            }

            for (int index = 0; index < Width * Height; index++)
            {
                if (background[index])
                    continue;

                int byteIndex = index * 4;
                output[byteIndex] = input.Bgra[byteIndex];
                output[byteIndex + 1] = input.Bgra[byteIndex + 1];
                output[byteIndex + 2] = input.Bgra[byteIndex + 2];

                int x = index % Width;
                int y = index / Width;
                bool bordersBackground =
                    (x > 0 && background[index - 1]) ||
                    (x + 1 < Width && background[index + 1]) ||
                    (y > 0 && background[index - Width]) ||
                    (y + 1 < Height && background[index + Width]);
                int alpha = 255;
                if (bordersBackground)
                {
                    int blue = input.Bgra[byteIndex];
                    int green = input.Bgra[byteIndex + 1];
                    int red = input.Bgra[byteIndex + 2];
                    int maximum = Math.Max(red, Math.Max(green, blue));
                    int minimum = Math.Min(red, Math.Min(green, blue));
                    int chroma = maximum - minimum;
                    if (minimum >= 170 && chroma <= 35)
                        alpha = Math.Min(255, chroma * 9 + Math.Max(0, 242 - minimum) * 4);
                }
                output[byteIndex + 3] = (byte)alpha;
            }

            WritePixels(output, destination);
        }
    }

    private static Registration FindRegistration(Pixels reference, Pixels generated)
    {
        Registration best = new Registration {
            SampleScale = 1.0,
            SampleDx = 0,
            SampleDy = 0,
            Score = Double.NegativeInfinity
        };

        // Start with a coarse translation pass. Some otherwise usable edits
        // move the redrawn head by twenty source pixels even though the canvas
        // dimensions and full-body baseline remain unchanged.
        for (int dy = -32; dy <= 32; dy += 2)
        {
            for (int dx = -32; dx <= 32; dx += 2)
            {
                double score = RegistrationScore(
                    reference, generated, 1.0, dx, dy, 6);
                if (score > best.Score)
                {
                    best.SampleScale = 1.0;
                    best.SampleDx = dx;
                    best.SampleDy = dy;
                    best.Score = score;
                }
            }
        }

        Registration coarseBest = best;
        for (int dy = coarseBest.SampleDy - 4; dy <= coarseBest.SampleDy + 4; dy++)
        {
            for (int dx = coarseBest.SampleDx - 4; dx <= coarseBest.SampleDx + 4; dx++)
            {
                double score = RegistrationScore(
                    reference, generated, 1.0, dx, dy, 3);
                if (score > best.Score)
                {
                    best.SampleScale = 1.0;
                    best.SampleDx = dx;
                    best.SampleDy = dy;
                    best.Score = score;
                }
            }
        }

        // Search only a small neighbourhood around the refined translation for
        // the sub-percent scale drift seen in generated masters.
        Registration translatedBest = best;
        for (int scaleStep = -4; scaleStep <= 4; scaleStep++)
        {
            double scale = 1.0 + scaleStep * 0.005;
            for (int dy = translatedBest.SampleDy - 3; dy <= translatedBest.SampleDy + 3; dy++)
            {
                for (int dx = translatedBest.SampleDx - 3; dx <= translatedBest.SampleDx + 3; dx++)
                {
                    double score = RegistrationScore(
                        reference, generated, scale, dx, dy, 3);
                    if (score > best.Score)
                    {
                        best.SampleScale = scale;
                        best.SampleDx = dx;
                        best.SampleDy = dy;
                        best.Score = score;
                    }
                }
            }
        }

        // Strong eye-direction changes (notably Embarrassed) replace enough of
        // the face-edge signal to lower NCC while the unchanged hair/glasses
        // still provide a stable fit. Anything below 0.35 remains a hard stop.
        if (best.Score < 0.35)
            throw new InvalidDataException(
                "Face registration confidence is too low for automatic extraction: "
                + best.Score.ToString("0.000"));
        if (Math.Abs(best.SampleDx) > 32 || Math.Abs(best.SampleDy) > 32)
            throw new InvalidDataException("Face registration exceeded the safe translation range.");

        return best;
    }

    private static double RegistrationScore(
        Pixels reference,
        Pixels generated,
        double scale,
        int dx,
        int dy,
        int sampleStep)
    {
        double sumReference = 0.0;
        double sumGenerated = 0.0;
        double sumReferenceSquared = 0.0;
        double sumGeneratedSquared = 0.0;
        double sumProduct = 0.0;
        int count = 0;

        for (int y = 150; y <= 500; y += sampleStep)
        {
            for (int x = 330; x <= 700; x += sampleStep)
            {
                int referenceIndex = y * Width + x;
                if (reference.Bgra[referenceIndex * 4 + 3] < 128)
                    continue;

                int generatedX = (int)Math.Round(
                    FaceCenterX + (x - FaceCenterX) * scale + dx);
                int generatedY = (int)Math.Round(
                    FaceCenterY + (y - FaceCenterY) * scale + dy);
                if (generatedX < 1 || generatedY < 1 ||
                    generatedX >= Width - 1 || generatedY >= Height - 1)
                    continue;

                double a = reference.Edge[referenceIndex];
                double b = generated.Edge[generatedY * Width + generatedX];
                sumReference += a;
                sumGenerated += b;
                sumReferenceSquared += a * a;
                sumGeneratedSquared += b * b;
                sumProduct += a * b;
                count++;
            }
        }

        double numerator = count * sumProduct - sumReference * sumGenerated;
        double referenceVariance = count * sumReferenceSquared
            - sumReference * sumReference;
        double generatedVariance = count * sumGeneratedSquared
            - sumGenerated * sumGenerated;
        double denominator = Math.Sqrt(referenceVariance * generatedVariance);
        return denominator <= 0.0 ? Double.NegativeInfinity : numerator / denominator;
    }

    private static Pixels ReadPixels(Bitmap bitmap)
    {
        var rectangle = new Rectangle(0, 0, Width, Height);
        BitmapData data = bitmap.LockBits(
            rectangle, ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
        try
        {
            byte[] packed = new byte[Width * Height * 4];
            for (int y = 0; y < Height; y++)
            {
                IntPtr row = IntPtr.Add(data.Scan0, y * data.Stride);
                Marshal.Copy(row, packed, y * Width * 4, Width * 4);
            }

            double[] luminance = new double[Width * Height];
            double[] edge = new double[Width * Height];
            for (int index = 0; index < Width * Height; index++)
            {
                int byteIndex = index * 4;
                luminance[index] = packed[byteIndex + 2] * 0.299
                    + packed[byteIndex + 1] * 0.587
                    + packed[byteIndex] * 0.114;
            }
            for (int y = 1; y < Height - 1; y++)
            {
                for (int x = 1; x < Width - 1; x++)
                {
                    int index = y * Width + x;
                    edge[index] = Math.Abs(luminance[index + 1] - luminance[index - 1])
                        + Math.Abs(luminance[index + Width] - luminance[index - Width]);
                }
            }
            return new Pixels(packed, edge);
        }
        finally
        {
            bitmap.UnlockBits(data);
        }
    }

    private static void WritePixels(byte[] pixels, string destination)
    {
        using (var output = new Bitmap(Width, Height, PixelFormat.Format32bppArgb))
        {
            var rectangle = new Rectangle(0, 0, Width, Height);
            BitmapData data = output.LockBits(
                rectangle, ImageLockMode.WriteOnly, PixelFormat.Format32bppArgb);
            try
            {
                for (int y = 0; y < Height; y++)
                {
                    IntPtr row = IntPtr.Add(data.Scan0, y * data.Stride);
                    Marshal.Copy(pixels, y * Width * 4, row, Width * 4);
                }
            }
            finally
            {
                output.UnlockBits(data);
            }
            output.Save(destination, ImageFormat.Png);
        }
    }

    private static Bitmap LoadArgb(string path)
    {
        using (var source = new Bitmap(path))
        {
            // Clone the pixel rectangle instead of drawing it onto a new
            // bitmap. GDI+ otherwise honours the PNG's embedded DPI here and
            // silently rescales the 1023x1537 source before registration.
            return source.Clone(
                new Rectangle(0, 0, Width, Height),
                PixelFormat.Format32bppArgb);
        }
    }

    private static void ValidateCanvas(string path)
    {
        using (var bitmap = new Bitmap(path))
        {
            if (bitmap.Width != Width || bitmap.Height != Height)
                throw new InvalidDataException(String.Format(
                    "{0} is {1}x{2}; expected {3}x{4}.",
                    path, bitmap.Width, bitmap.Height, Width, Height));
        }
    }

    private static void SampleBilinear(
        byte[] source,
        double x,
        double y,
        byte[] destination,
        int destinationIndex)
    {
        int x0 = Math.Max(0, Math.Min(Width - 1, (int)Math.Floor(x)));
        int y0 = Math.Max(0, Math.Min(Height - 1, (int)Math.Floor(y)));
        int x1 = Math.Min(Width - 1, x0 + 1);
        int y1 = Math.Min(Height - 1, y0 + 1);
        double horizontal = Math.Max(0.0, Math.Min(1.0, x - x0));
        double vertical = Math.Max(0.0, Math.Min(1.0, y - y0));
        int topLeft = (y0 * Width + x0) * 4;
        int topRight = (y0 * Width + x1) * 4;
        int bottomLeft = (y1 * Width + x0) * 4;
        int bottomRight = (y1 * Width + x1) * 4;

        for (int channel = 0; channel < 3; channel++)
        {
            double top = source[topLeft + channel] * (1.0 - horizontal)
                + source[topRight + channel] * horizontal;
            double bottom = source[bottomLeft + channel] * (1.0 - horizontal)
                + source[bottomRight + channel] * horizontal;
            destination[destinationIndex + channel] = (byte)Math.Round(
                top * (1.0 - vertical) + bottom * vertical);
        }
    }

    private static bool IsBackgroundLike(byte[] pixels, int pixelIndex)
    {
        int byteIndex = pixelIndex * 4;
        int blue = pixels[byteIndex];
        int green = pixels[byteIndex + 1];
        int red = pixels[byteIndex + 2];
        int maximum = Math.Max(red, Math.Max(green, blue));
        int minimum = Math.Min(red, Math.Min(green, blue));
        return minimum >= 218 && maximum - minimum <= 14;
    }

    private static void EnqueueBackground(
        int x,
        int y,
        byte[] pixels,
        bool[] visited,
        Queue<int> queue)
    {
        if (x < 0 || y < 0 || x >= Width || y >= Height)
            return;
        int index = y * Width + x;
        if (visited[index])
            return;
        visited[index] = true;
        if (IsBackgroundLike(pixels, index))
            queue.Enqueue(index);
    }
}
'@

$expressions = @(
    "happy", "smug", "teasing", "thinking", "curious", "unamused",
    "annoyed", "frustrated", "angry", "sad", "crying", "embarrassed",
    "nervous", "worried", "shocked", "afraid", "panicked", "determined",
    "empty", "disgusted"
)

[HimekoSpriteProcessor]::CopyBase(
    $casualBase,
    (Join-Path $outputRoot "neut_face_base.png"))
[HimekoSpriteProcessor]::CopyBase(
    $uniformBase,
    (Join-Path $outputRoot "neut_uniform_face_base.png"))
[HimekoSpriteProcessor]::MakeTransparentFace(
    (Join-Path $outputRoot "face_neut.png"))

foreach ($expression in $expressions) {
    $source = Join-Path $sourceRoot ("expression_{0}.png" -f $expression)
    $destination = Join-Path $outputRoot ("face_{0}.png" -f $expression)
    $report = [HimekoSpriteProcessor]::MakeExpressionFace(
        $source,
        $casualBase,
        $uniformBase,
        $destination)
    Write-Output $report
}

# Pose export intentionally stops here. The canonical pose PNGs use a later
# soft-alpha/decontamination pass; RemoveCheckerboard above is retained only for
# provenance and would restore the old hard gray fringe if run against them.
