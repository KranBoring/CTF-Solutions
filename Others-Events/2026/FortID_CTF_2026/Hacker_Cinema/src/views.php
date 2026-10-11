<?php
require_once __DIR__ . '/config.php';

function h(mixed $value): string {
    return htmlspecialchars((string)$value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function layout_start(string $title): void {
    echo '<!doctype html><html lang="en"><head><meta charset="utf-8">';
    echo '<meta name="viewport" content="width=device-width, initial-scale=1">';
    echo '<title>' . h($title) . ' · Hacker Cinema</title>';
    echo '<link rel="stylesheet" href="/static/css/main.css">';
    echo '</head><body><header><div class="tagline">Access the mainframe. Claim the prize.</div><h1>HACKER CINEMA</h1></header>';
    echo '<nav><a href="/">Get tickets</a><a href="/check">Prize checker</a></nav><main>';
}

function layout_end(): void {
    echo '</main></body></html>';
}

function seat_grid(): array {
    $grid = [];
    foreach (str_split('ABCDEF') as $row) {
        $line = [];
        for ($col = 1; $col <= 12; $col++) {
            $line[] = sprintf('%s%02d', $row, $col);
        }
        $grid[] = $line;
    }
    return $grid;
}

function render_index(string $minDate, string $defaultDate, int $defaultTs, string $error = ''): void {
    layout_start('Now Showing');
    echo '<div class="grid"><section class="panel poster"><div class="poster-content">';
    echo '<div class="movie-title">Hackers</div><div class="movie-year">One show every day · ' . sprintf('%02d', SHOW_HOUR_UTC) . ':00 UTC</div>';
    echo '<p class="hint">Zero Cool. Acid Burn. One movie. Infinite fun.</p></div></section>';
    echo '<section class="panel"><h2>Get a free ticket</h2>';
    if ($error !== '') echo '<p class="bad">' . h($error) . '</p>';
    echo '<form method="post" action="/buy">';
    echo '<label for="show_date">Screening date</label>';
    echo '<input type="date" id="show_date" name="show_date" min="' . h($minDate) . '" value="' . h($defaultDate) . '" required>';
    echo '<p class="hint">Pick any upcoming screening. Doors open 15 minutes before showtime.</p>';
    echo '<div class="screen">SCREEN MAINFRAME-1</div><div class="seats">';
    foreach (seat_grid() as $row) {
        foreach ($row as $seat) {
            $checked = $seat === 'C07' ? ' checked' : '';
            echo '<label class="seat"><input type="radio" name="seat" value="' . h($seat) . '"' . $checked . '><span>' . h($seat) . '</span></label>';
        }
    }
    echo '</div><button type="submit">Get a free ticket</button></form></section></div>';
    layout_end();
}

function render_ticket(string $ticketId, ?array $ticket): void {
    layout_start('Ticket');
    echo '<div class="grid"><section class="panel"><h2>Your ticket is ready</h2>';
    if ($ticket !== null) {
        echo '<p class="hint">' . h($ticket['movie'] ?? MOVIE) . ' · ' . h($ticket['date'] ?? '') . ' · Seat ' . h($ticket['seat'] ?? '') . '</p>';
    }
    echo '<div class="ticket-preview"><img alt="Printable Hacker Cinema ticket" src="/ticket.png?id=' . h($ticketId) . '"></div>';
    echo '<div class="actions"><a class="button-link" href="/ticket.png?id=' . h($ticketId) . '&download=1" download="hacker-cinema-ticket.png">Download ticket</a>';
    echo '<a class="button-link secondary" href="/">Back to seats</a></div></section>';
    echo '<section class="panel"><h2>Before you arrive</h2><ul>';
    echo '<li>Please arrive at least 15 minutes before showtime.</li>';
    echo '<li>Outside food and drinks are not allowed in the theater.</li>';
    echo '<li>Neon Nachos, Crash Override Cola, and popcorn are available at concessions.</li>';
    echo '<li>Keep your QR ticket ready for entry and prize checks.</li>';
    echo '</ul><a class="button-link" href="/check">Open prize checker</a></section></div>';
    layout_end();
}

function render_ticket_expired(): void {
    layout_start('Ticket Expired');
    echo '<div class="panel"><h2>Ticket expired</h2><p class="hint">The kiosk no longer has that ticket in its print queue. Please return to seat selection and print a fresh one.</p>';
    echo '<a class="button-link" href="/">Back to seat selection</a></div>';
    layout_end();
}

function render_check(string $error = '', string $success = '', string $flag = ''): void {
    layout_start('Prize Checker');
    echo '<div class="panel"><h2>Neon prize checker</h2>';
    echo '<p class="hint">Upload a photo or screenshot of your Hacker Cinema QR ticket to see whether it won tonight\'s promo prize.</p>';
    if ($error !== '') echo '<p class="bad">' . h($error) . '</p>';
    if ($success !== '') echo '<p class="ok">' . h($success) . '</p>';
    if ($flag !== '') echo '<pre>' . h($flag) . '</pre>';
    echo '<form method="post" action="/check" enctype="multipart/form-data">';
    echo '<label for="qr">QR ticket image</label><input id="qr" name="qr" type="file" accept="image/png,image/jpeg" required>';
    echo '<button type="submit">Check ticket</button></form></div>';
    layout_end();
}
