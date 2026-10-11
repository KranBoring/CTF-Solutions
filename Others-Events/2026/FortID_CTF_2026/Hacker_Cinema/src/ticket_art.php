<?php
require_once __DIR__ . '/config.php';

function tmp_png_path(string $prefix): string {
    return sys_get_temp_dir() . DIRECTORY_SEPARATOR . $prefix . bin2hex(random_bytes(8)) . '.png';
}

function qr_png_bytes(string $payload, int $boxSize = 7): string {
    $tmp = tmp_png_path('hcinema_qr_');
    $cmd = sprintf('qrencode -m 2 -s %d -o %s %s 2>/dev/null', $boxSize, escapeshellarg($tmp), escapeshellarg($payload));
    shell_exec($cmd);
    if (!is_file($tmp)) {
        throw new RuntimeException('ticket printer could not generate a QR code');
    }
    $bytes = file_get_contents($tmp);
    @unlink($tmp);
    return $bytes;
}

function decode_qr_image(string $imageBytes): string {
    $tmp = tmp_png_path('hcinema_scan_');
    file_put_contents($tmp, $imageBytes);
    $cmd = sprintf('zbarimg --raw -q %s 2>/dev/null', escapeshellarg($tmp));
    $out = shell_exec($cmd);
    @unlink($tmp);
    if ($out === null || trim($out) === '') {
        throw new InvalidArgumentException('no QR code found in uploaded image');
    }
    $line = strtok($out, "\r\n");
    return $line === false ? trim($out) : $line;
}

function gd_color(GdImage $img, string $hex): int {
    $hex = ltrim($hex, '#');
    return imagecolorallocate($img, hexdec(substr($hex, 0, 2)), hexdec(substr($hex, 2, 2)), hexdec(substr($hex, 4, 2)));
}

function font_path(bool $bold = false): ?string {
    $candidates = $bold ? [
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    ] : [
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ];
    foreach ($candidates as $path) {
        if (is_file($path)) return $path;
    }
    return null;
}

function draw_text(GdImage $img, int $size, int $x, int $y, string $text, int $color, bool $bold = false): void {
    $font = font_path($bold);
    if ($font !== null) {
        imagettftext($img, $size, 0, $x, $y, $color, $font, $text);
    } else {
        imagestring($img, min(5, max(1, intdiv($size, 6))), $x, $y - $size, $text, $color);
    }
}

function draw_center_text(GdImage $img, int $size, int $cx, int $cy, string $text, int $color, bool $bold = false): void {
    $font = font_path($bold);
    if ($font !== null) {
        $box = imagettfbbox($size, 0, $font, $text);
        $w = abs($box[2] - $box[0]);
        $h = abs($box[7] - $box[1]);
        imagettftext($img, $size, 0, $cx - intdiv($w, 2), $cy + intdiv($h, 2), $color, $font, $text);
    } else {
        imagestring($img, 3, $cx - strlen($text) * 4, $cy - 7, $text, $color);
    }
}

function ticket_image_bytes(string $payload): string {
    if (!extension_loaded('gd')) {
        throw new RuntimeException('ticket printer requires the PHP GD extension');
    }
    $env = json_decode($payload, true);
    $ticket = is_array($env['ticket'] ?? null) ? $env['ticket'] : [];
    $date = (string)($ticket['date'] ?? '????-??-??');
    $seat = (string)($ticket['seat'] ?? '??');
    $screen = strtoupper((string)($ticket['screen'] ?? SCREEN));
    $movie = strtoupper((string)($ticket['movie'] ?? MOVIE));

    $width = 1120;
    $height = 460;
    $img = imagecreatetruecolor($width, $height);
    imageantialias($img, true);

    $paper = gd_color($img, '#fff7df');
    $ink = gd_color($img, '#101018');
    $pink = gd_color($img, '#ff2bd6');
    $cyan = gd_color($img, '#27f7ff');
    $green = gd_color($img, '#39ff88');
    $muted = gd_color($img, '#55556a');
    $dark = gd_color($img, '#333348');
    $white = gd_color($img, '#ffffff');

    imagefilledrectangle($img, 0, 0, $width, $height, $paper);
    imagerectangle($img, 18, 18, $width - 18, $height - 18, $ink);
    imagerectangle($img, 19, 19, $width - 19, $height - 19, $ink);
    imagefilledrectangle($img, 20, 20, 92, $height - 20, $ink);
    imagefilledrectangle($img, 92, 20, 102, $height - 20, $pink);
    imagefilledrectangle($img, 102, 20, 108, $height - 20, $cyan);

    for ($y = 42; $y < $height - 42; $y += 22) {
        imageline($img, 760, $y, 760, $y + 10, $ink);
        imageline($img, 761, $y, 761, $y + 10, $ink);
    }

    $stripY = 105;
    foreach (['HACK', 'THE', 'PLANET'] as $line) {
        draw_center_text($img, 13, 56, $stripY, $line, $cyan, true);
        $stripY += 68;
    }

    draw_text($img, 48, 140, 86, 'HACKER CINEMA', $ink, true);
    draw_text($img, 22, 144, 122, 'ADMIT ONE · FREE SCREENING', $pink, true);
    imageline($img, 140, 152, 710, 152, $ink);
    imageline($img, 140, 153, 710, 153, $ink);

    draw_text($img, 18, 140, 208, 'MOVIE', $muted, true);
    draw_text($img, 26, 140, 246, $movie . ' (' . MOVIE_YEAR . ')', $ink, true);

    draw_text($img, 18, 140, 298, 'DATE', $muted, true);
    draw_text($img, 26, 140, 336, $date, $ink, true);

    draw_text($img, 18, 380, 298, 'TIME', $muted, true);
    draw_text($img, 26, 380, 336, sprintf('%02d:00 UTC', SHOW_HOUR_UTC), $ink, true);

    draw_text($img, 18, 620, 298, 'SEAT', $muted, true);
    draw_text($img, 26, 620, 336, $seat, $ink, true);

    draw_text($img, 22, 140, 402, 'SCREEN ' . $screen, $ink, true);
    draw_text($img, 14, 140, 432, 'Doors open 15 minutes before showtime. Keep this ticket ready.', $dark, false);

    $stubLeft = 796;
    $stubRight = 1068;
    $stubCenter = intdiv($stubLeft + $stubRight, 2);
    imagefilledrectangle($img, $stubLeft, 48, $stubRight, 102, $ink);
    draw_center_text($img, 20, $stubCenter, 78, 'SCAN TICKET', $cyan, true);

    $qrPanelX = 800;
    $qrPanelY = 122;
    $qrPanelSize = 264;
    $qrPadding = 12;
    $qrSize = $qrPanelSize - ($qrPadding * 2);
    imagefilledrectangle($img, $qrPanelX, $qrPanelY, $qrPanelX + $qrPanelSize, $qrPanelY + $qrPanelSize, $white);
    imagerectangle($img, $qrPanelX, $qrPanelY, $qrPanelX + $qrPanelSize, $qrPanelY + $qrPanelSize, $ink);
    imagerectangle($img, $qrPanelX + 1, $qrPanelY + 1, $qrPanelX + $qrPanelSize - 1, $qrPanelY + $qrPanelSize - 1, $ink);

    $qrBytes = qr_png_bytes($payload, 5);
    $qr = imagecreatefromstring($qrBytes);
    if (!$qr) {
        throw new RuntimeException('ticket printer could not compose the QR code');
    }
    imagecopyresampled($img, $qr, $qrPanelX + $qrPadding, $qrPanelY + $qrPadding, 0, 0, $qrSize, $qrSize, imagesx($qr), imagesy($qr));
    imagedestroy($qr);
    draw_center_text($img, 12, $stubCenter, 424, 'Hacker Cinema · Mainframe-1', $dark, false);

    ob_start();
    imagepng($img);
    $bytes = (string)ob_get_clean();
    imagedestroy($img);
    return $bytes;
}
