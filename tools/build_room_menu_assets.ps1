Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$outputDirectory = Join-Path $projectRoot "game\assets\gui\menu\room_theme"
[System.IO.Directory]::CreateDirectory($outputDirectory) | Out-Null

function New-RoomSelectorAsset {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        [Parameter(Mandatory = $true)]
        [System.Drawing.Color]$TopColor,
        [Parameter(Mandatory = $true)]
        [System.Drawing.Color]$BottomColor,
        [Parameter(Mandatory = $true)]
        [System.Drawing.Color]$BorderColor,
        [Parameter(Mandatory = $true)]
        [System.Drawing.Color]$AccentColor,
        [Parameter(Mandatory = $true)]
        [System.Drawing.Color]$ThreadColor
    )

    $width = 112
    $height = 56
    $bitmap = New-Object System.Drawing.Bitmap($width, $height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $graphics.Clear([System.Drawing.Color]::Transparent)

    $shape = New-Object System.Drawing.Drawing2D.GraphicsPath
    $shape.AddPolygon([System.Drawing.Point[]]@(
        [System.Drawing.Point]::new(0, 8),
        [System.Drawing.Point]::new(8, 0),
        [System.Drawing.Point]::new(96, 0),
        [System.Drawing.Point]::new(112, 16),
        [System.Drawing.Point]::new(112, 48),
        [System.Drawing.Point]::new(104, 56),
        [System.Drawing.Point]::new(12, 56),
        [System.Drawing.Point]::new(0, 44)
    ))

    $gradient = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
        [System.Drawing.Rectangle]::new(0, 0, $width, $height),
        $TopColor,
        $BottomColor,
        90.0
    )
    $graphics.FillPath($gradient, $shape)

    $borderPen = New-Object System.Drawing.Pen($BorderColor, 1.4)
    $graphics.DrawPath($borderPen, $shape)

    $innerPen = New-Object System.Drawing.Pen($ThreadColor, 1.0)
    $innerPen.DashPattern = [single[]]@(2.0, 3.0)
    $graphics.DrawLine($innerPen, 12, 7, 94, 7)
    $graphics.DrawLine($innerPen, 15, 49, 99, 49)

    $accentBrush = New-Object System.Drawing.SolidBrush($AccentColor)
    $graphics.FillPolygon($accentBrush, [System.Drawing.Point[]]@(
        [System.Drawing.Point]::new(0, 8),
        [System.Drawing.Point]::new(5, 3),
        [System.Drawing.Point]::new(5, 49),
        [System.Drawing.Point]::new(0, 44)
    ))
    $graphics.FillPolygon($accentBrush, [System.Drawing.Point[]]@(
        [System.Drawing.Point]::new(96, 0),
        [System.Drawing.Point]::new(112, 16),
        [System.Drawing.Point]::new(106, 16),
        [System.Drawing.Point]::new(96, 6)
    ))

    $outputPath = Join-Path $outputDirectory $Name
    $bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

    $accentBrush.Dispose()
    $innerPen.Dispose()
    $borderPen.Dispose()
    $gradient.Dispose()
    $shape.Dispose()
    $graphics.Dispose()
    $bitmap.Dispose()
}

New-RoomSelectorAsset `
    -Name "selector_idle.png" `
    -TopColor ([System.Drawing.Color]::FromArgb(218, 15, 26, 31)) `
    -BottomColor ([System.Drawing.Color]::FromArgb(230, 25, 38, 41)) `
    -BorderColor ([System.Drawing.Color]::FromArgb(155, 110, 151, 150)) `
    -AccentColor ([System.Drawing.Color]::FromArgb(225, 89, 159, 153)) `
    -ThreadColor ([System.Drawing.Color]::FromArgb(75, 230, 215, 188))

New-RoomSelectorAsset `
    -Name "selector_hover.png" `
    -TopColor ([System.Drawing.Color]::FromArgb(236, 31, 61, 62)) `
    -BottomColor ([System.Drawing.Color]::FromArgb(240, 62, 38, 47)) `
    -BorderColor ([System.Drawing.Color]::FromArgb(225, 227, 205, 174)) `
    -AccentColor ([System.Drawing.Color]::FromArgb(255, 208, 103, 91)) `
    -ThreadColor ([System.Drawing.Color]::FromArgb(120, 244, 229, 203))

New-RoomSelectorAsset `
    -Name "selector_selected.png" `
    -TopColor ([System.Drawing.Color]::FromArgb(242, 45, 86, 84)) `
    -BottomColor ([System.Drawing.Color]::FromArgb(244, 76, 43, 55)) `
    -BorderColor ([System.Drawing.Color]::FromArgb(245, 237, 220, 191)) `
    -AccentColor ([System.Drawing.Color]::FromArgb(255, 224, 132, 83)) `
    -ThreadColor ([System.Drawing.Color]::FromArgb(150, 250, 235, 209))

New-RoomSelectorAsset `
    -Name "selector_danger.png" `
    -TopColor ([System.Drawing.Color]::FromArgb(238, 76, 36, 45)) `
    -BottomColor ([System.Drawing.Color]::FromArgb(242, 112, 48, 49)) `
    -BorderColor ([System.Drawing.Color]::FromArgb(235, 239, 185, 157)) `
    -AccentColor ([System.Drawing.Color]::FromArgb(255, 232, 119, 91)) `
    -ThreadColor ([System.Drawing.Color]::FromArgb(125, 255, 222, 190))

# Confirmation choices need state changes that remain obvious through the
# modal scrim. These plates keep each choice's meaning while brightening its
# own colour family instead of sending both buttons through the generic hover.
New-RoomSelectorAsset `
    -Name "selector_yes_hover.png" `
    -TopColor ([System.Drawing.Color]::FromArgb(255, 126, 49, 55)) `
    -BottomColor ([System.Drawing.Color]::FromArgb(255, 160, 67, 58)) `
    -BorderColor ([System.Drawing.Color]::FromArgb(255, 255, 226, 197)) `
    -AccentColor ([System.Drawing.Color]::FromArgb(255, 255, 151, 91)) `
    -ThreadColor ([System.Drawing.Color]::FromArgb(205, 255, 241, 216))

New-RoomSelectorAsset `
    -Name "selector_no_hover.png" `
    -TopColor ([System.Drawing.Color]::FromArgb(255, 58, 122, 116)) `
    -BottomColor ([System.Drawing.Color]::FromArgb(255, 103, 62, 78)) `
    -BorderColor ([System.Drawing.Color]::FromArgb(255, 240, 225, 199)) `
    -AccentColor ([System.Drawing.Color]::FromArgb(255, 235, 150, 84)) `
    -ThreadColor ([System.Drawing.Color]::FromArgb(195, 255, 242, 218))

Write-Output "Built room-menu selector assets in $outputDirectory"
