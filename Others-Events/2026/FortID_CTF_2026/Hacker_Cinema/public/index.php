<?php
declare(strict_types=1);

if (PHP_SAPI === 'cli-server') {
    $staticPath = __DIR__ . (parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/');
    if (is_file($staticPath)) {
        return false;
    }
}

require_once __DIR__ . '/../src/config.php';
require_once __DIR__ . '/../src/calendar.php';
require_once __DIR__ . '/../src/store.php';
require_once __DIR__ . '/../src/tickets.php';
require_once __DIR__ . '/../src/ticket_art.php';
require_once __DIR__ . '/../src/views.php';

function redirect_to(string $path, int $status = 302): never {
    http_response_code($status);
    header('Location: ' . $path);
    exit;
}

function read_flag(): string {
    $value = getenv('FLAG');
    if ($value !== false && $value !== '') {
        return $value;
    }
    $path = flag_path();
    if (!is_file($path)) {
        return 'FORTID{dummy_flag_missing_flag_txt}';
    }
    return trim((string)file_get_contents($path));
}

function request_path(): string {
    return parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
}

try {
    $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
    $path = request_path();

    if ($method === 'GET' && $path === '/') {
        [$minDate, $defaultDate, $defaultTs] = future_dates();
        render_index($minDate, $defaultDate, $defaultTs, (string)($_GET['error'] ?? ''));
        exit;
    }

    if ($method === 'POST' && $path === '/buy') {
        $seat = (string)($_POST['seat'] ?? '');
        $screeningRaw = trim((string)($_POST['screening'] ?? ''));
        $showDateRaw = trim((string)($_POST['show_date'] ?? ''));
        if (!preg_match(SEAT_RE, $seat)) {
            redirect_to('/?error=' . rawurlencode('Unknown seat.'), 303);
        }
        try {
            if ($screeningRaw !== '') {
                if (!preg_match('/^-?\d+$/', $screeningRaw)) {
                    throw new InvalidArgumentException('invalid timestamp');
                }
                $screeningTs = (int)$screeningRaw;
            } else {
                $screeningTs = timestamp_for_show_date($showDateRaw);
            }
        } catch (Throwable) {
            redirect_to('/?error=' . rawurlencode('The ticket kiosk could not read that screening date.'), 303);
        }
        if ($screeningTs < MIN_SCREENING_TS || $screeningTs > MAX_SCREENING_TS) {
            redirect_to('/?error=' . rawurlencode('That screening is outside the cinema schedule.'), 303);
        }
        [, $payload] = make_ticket($seat, $screeningTs);
        $id = put_ticket($payload);
        redirect_to('/ticket?id=' . rawurlencode($id), 303);
    }

    if ($method === 'GET' && $path === '/ticket') {
        $id = (string)($_GET['id'] ?? '');
        $payload = get_ticket($id);
        if ($payload === null) {
            render_ticket_expired();
            exit;
        }
        $env = json_decode($payload, true);
        $ticket = is_array($env['ticket'] ?? null) ? $env['ticket'] : null;
        render_ticket($id, $ticket);
        exit;
    }

    if ($method === 'GET' && $path === '/ticket.png') {
        $id = (string)($_GET['id'] ?? '');
        $payload = get_ticket($id);
        if ($payload === null) {
            http_response_code(404);
            header('Content-Type: text/plain; charset=utf-8');
            echo 'ticket expired';
            exit;
        }
        $bytes = ticket_image_bytes($payload);
        header('Content-Type: image/png');
        header('Cache-Control: no-store');
        if (($_GET['download'] ?? '') === '1') {
            header('Content-Disposition: attachment; filename="hacker-cinema-ticket.png"');
        }
        echo $bytes;
        exit;
    }

    if ($method === 'GET' && $path === '/check') {
        render_check();
        exit;
    }

    if ($method === 'POST' && $path === '/check') {
        try {
            if (!isset($_FILES['qr']) || !is_uploaded_file($_FILES['qr']['tmp_name'])) {
                throw new InvalidArgumentException('missing QR ticket image');
            }
            $payload = decode_qr_image((string)file_get_contents($_FILES['qr']['tmp_name']));
            [$ticket, $valid] = verify_envelope($payload);
            if (!$valid) {
                render_check('Ticket rejected. Please visit the box office.');
                exit;
            }
            if (($ticket['movie'] ?? '') === MOVIE && ($ticket['screen'] ?? '') === SCREEN && ($ticket['winner'] ?? false) === true) {
                render_check('', 'JACKPOT ACCEPTED.', read_flag());
                exit;
            }
            render_check('', 'Valid ticket. Enjoy the movie. No prize on this one.');
            exit;
        } catch (Throwable $e) {
            http_response_code(400);
            render_check('Could not scan ticket: ' . $e->getMessage());
            exit;
        }
    }

    http_response_code(404);
    layout_start('Not Found');
    echo '<div class="panel"><h2>404</h2><p class="hint">That theater corridor is closed.</p><a class="button-link" href="/">Back to lobby</a></div>';
    layout_end();
} catch (Throwable $e) {
    http_response_code(500);
    layout_start('Kiosk Error');
    echo '<div class="panel"><h2>Kiosk error</h2><p class="bad">The ticket kiosk glitched. Please try again.</p></div>';
    layout_end();
}
