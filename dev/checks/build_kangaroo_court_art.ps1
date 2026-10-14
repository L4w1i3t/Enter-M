param([string]$ManifestPath = 'docs/assets/kangaroo_court/sprite_manifest.json')
$ErrorActionPreference = 'Stop'
$project = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
function ProjectPath([string]$relative) {
    $resolved = [IO.Path]::GetFullPath((Join-Path $project $relative))
    if (-not $resolved.StartsWith($project + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw "Path outside project: $relative" }
    return $resolved
}
$manifest = Get-Content -LiteralPath (ProjectPath $ManifestPath) -Raw | ConvertFrom-Json
if ($manifest.version -ne 2) { throw 'Expected native-alpha manifest version 2.' }
Add-Type -AssemblyName System.Drawing
Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @'
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Drawing.Drawing2D;
using System.Runtime.InteropServices;
public static class KCArt {
    public static int[] Inspect(Bitmap b) {
        var data = b.LockBits(new Rectangle(0,0,b.Width,b.Height), ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
        byte[] bytes = new byte[Math.Abs(data.Stride)*b.Height];
        Marshal.Copy(data.Scan0,bytes,0,bytes.Length);
        int lo=255, hi=0, visible=0, partial=0, left=b.Width, top=b.Height, right=0, bottom=0, border=0;
        for(int y=0;y<b.Height;y++) for(int x=0;x<b.Width;x++) {
            int a=bytes[y*data.Stride+x*4+3]; lo=Math.Min(lo,a); hi=Math.Max(hi,a);
            if(a>0 && a<255) partial++;
            if(a>=8) { visible++; left=Math.Min(left,x); top=Math.Min(top,y); right=Math.Max(right,x+1); bottom=Math.Max(bottom,y+1); if(x==0||y==0||x==b.Width-1||y==b.Height-1) border++; }
        }
        b.UnlockBits(data);
        return new int[]{lo,hi,visible,partial,left,top,right,bottom,border};
    }
    public static int[] Register(string source,string output,float scale,float x,float y) {
        using(var input=new Bitmap(source)) using(var stage=new Bitmap(1280,720,PixelFormat.Format32bppArgb)) {
            var src=Inspect(input);
            if(src[0]!=0||src[1]!=255||src[2]==0) throw new Exception("Source must have genuine alpha: "+source);
            if(x+src[4]*scale<0||y+src[5]*scale<0||x+src[6]*scale>1280||y+src[7]*scale>720) throw new Exception("Registration clips source: "+source);
            using(var g=Graphics.FromImage(stage)) using(var attrs=new ImageAttributes()) {
                g.Clear(Color.Transparent); g.CompositingMode=CompositingMode.SourceCopy;
                g.InterpolationMode=InterpolationMode.HighQualityBicubic; g.PixelOffsetMode=PixelOffsetMode.HighQuality;
                attrs.SetWrapMode(WrapMode.TileFlipXY);
                g.DrawImage(input,Rectangle.Round(new RectangleF(x,y,input.Width*scale,input.Height*scale)),0,0,input.Width,input.Height,GraphicsUnit.Pixel,attrs);
            }
            var stats=Inspect(stage);
            if(stats[8]!=0) throw new Exception("Visible stage edge clipping: "+output);
            stage.Save(output,ImageFormat.Png); return stats;
        }
    }
    public static void Preview(string sprite,string background,string output) {
        using(var b=new Bitmap(1280,720,PixelFormat.Format32bppArgb)) using(var g=Graphics.FromImage(b)) using(var s=new Bitmap(sprite)) {
            g.InterpolationMode=InterpolationMode.HighQualityBicubic;
            if(background=="light") g.Clear(Color.FromArgb(235,235,235));
            else if(background=="dark") g.Clear(Color.FromArgb(28,32,42));
            else using(var bg=new Bitmap(background)) g.DrawImage(bg,0,0,1280,720);
            g.DrawImageUnscaled(s,0,0); b.Save(output,ImageFormat.Png);
        }
    }
    public static void Mask(string output,Point[] points) {
        using(var b=new Bitmap(1280,720,PixelFormat.Format32bppArgb)) using(var g=Graphics.FromImage(b)) {
            g.Clear(Color.Transparent); g.FillPolygon(Brushes.White,points); b.Save(output,ImageFormat.Png);
        }
    }
}
'@
$review = ProjectPath $manifest.review_directory
New-Item -ItemType Directory -Force -Path $review | Out-Null
$stats = @()
foreach ($sprite in $manifest.sprites) {
    $source = ProjectPath $sprite.source
    $output = ProjectPath $sprite.output
    if ($source -eq $output) { throw 'Input and output must differ.' }
    $values = [KCArt]::Register($source,$output,$sprite.scale,$sprite.x,$sprite.y)
    [KCArt]::Preview($output,(ProjectPath $sprite.preview_background),(Join-Path $review ($sprite.id + '.png')))
    [KCArt]::Preview($output,'light',(Join-Path $review ($sprite.id + '_light.png')))
    [KCArt]::Preview($output,'dark',(Join-Path $review ($sprite.id + '_dark.png')))
    $stats += [ordered]@{id=$sprite.id;source_sha256=(Get-FileHash -LiteralPath $source).Hash;output_sha256=(Get-FileHash -LiteralPath $output).Hash;alpha_min=$values[0];alpha_max=$values[1];visible_pixels=$values[2];partial_alpha_pixels=$values[3];bounds=@($values[4],$values[5],$values[6],$values[7]);edge_pixels=$values[8]}
}
foreach ($mask in $manifest.masks) {
    $points = @($mask.points | ForEach-Object { [Drawing.Point]::new($_[0],$_[1]) })
    [KCArt]::Mask((ProjectPath $mask.output),[Drawing.Point[]]$points)
}
$stats | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $review 'registration-stats.json') -Encoding UTF8
Write-Output "Registered $($stats.Count) native-alpha sprites; rebuilt $($manifest.masks.Count) masks."
