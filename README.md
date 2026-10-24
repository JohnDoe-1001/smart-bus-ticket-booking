# Smart Bus Ticket Booking & Reservation System (v2)

## Executive Summary
The **Smart Bus Ticket Booking & Reservation System** is a pure Python 3 console-based transportation management application designed to manage routes, passenger details, seat reservations, cancellations, schedules, and analytics reports in memory.

---

## Features & Capabilities
1. **View Available Routes**: Displays active bus routes with departure times, fares, and real-time seat availability (`available/total`).
2. **Search for a Route**: Case-insensitive lookup by Route ID, Departure City, or Destination City using normalized inputs (`.lower()`).
3. **Book a Ticket**: Secure booking engine enforcing passenger name validation, positive age/seat checks, route existence, and capacity validation before issuing unique IDs (`B1001`, `B1002`).
4. **View Bookings**: History ledger tracking both `Confirmed` and `Cancelled` ticket records.
5. **Cancel a Booking**: One-time cancellation system that restores seat capacity directly to the target route while retaining booking history.
6. **Seat Availability**: Live seating capacity breakdown classifying routes as `Available`, `Partially Booked`, or `Fully Booked`.
7. **Route Schedules**: Multi-city schedule breakdown grouped by departure city using nested loops over supported cities.
8. **Booking Report & Analytics**: Financial and operational report displaying created, confirmed, and cancelled counts, reserved seats, confirmed revenue (excluding cancelled fares), and fully booked route counts.

---

## System Requirements & Setup

### Requirements
- **Language**: Python 3.8+
- **Dependencies**: Built-in standard Python libraries only (no external packages required)

### How to Run
1. Open your terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd smart_bus_system
   ```
3. Run the updated v2 application script:
   ```bash
   python3 main-v2.py
   ```

---

## Code Documentation & Function Standards
The implementation in `main-v2.py` follows clean code standards with standardized docstrings for every helper validator, core feature, and loop construct. Each function includes explicit bullet points detailing:
- **`• What it does`**: Explains the core business logic, iteration method, or validation check performed.
- **`• What it returns`**: Documents return types (`bool`, `None`, `dict`, `int`, etc.) and side effects on global state.

---

## UI Display & Formatting Mechanics
To render clean, aligned terminal tables without third-party dependencies, the application utilizes Python f-string **format specifiers** (`:<number`):
- **Syntax**: `f"{text:<28}"`
- **Function**: Left-aligns `text` within a fixed-width block of 28 characters, padding shorter strings with trailing spaces.
- **Purpose**: Guarantees perfectly aligned tabular columns across monospaced console interfaces regardless of varying city name or price lengths.

---

## Validation & Error Handling Architecture
When invalid inputs (blank names, non-positive age/seats, unknown route IDs, or overbooking requests) occur during booking:
1. **Single-Pass Rejection**: The system displays an explicit error message and immediately returns control to the main menu.
2. **Terminal Trap Prevention**: Prevents endless re-prompting loops that trap users if they enter the booking menu by mistake or change their mind.
3. **Data Atomicity**: State changes (`bookings.append()` and `available_seats -= seats`) execute **only** after every single validation check succeeds, ensuring zero partial or corrupted entries.

---

## Data Architecture & In-Memory Storage
All system records exist purely **in-memory** using standard Python built-in collections:
- **Routes (`routes`)**: `List[Dict]` containing starter routes `R101` through `R105`.
- **Bookings (`bookings`)**: `List[Dict]` storing passenger booking records.
- **Issued IDs (`issued_booking_ids`)**: `Set[str]` preventing duplicate ticket ID issuance.
- **Supported Cities (`supported_cities`)**: `Tuple[str]` defining valid hub locations.

> **Storage Limitation Note**: Data persists only for the duration of the execution session. When the application terminates, all booking records and availability updates reset to initial starter states.

---

## Business Rules & Logic Validation
- **BR-01**: Blank or whitespace passenger names are rejected.
- **BR-02 & BR-04**: Age and seat quantities must be integers > 0.
- **BR-03 & BR-05**: Bookings require valid route IDs and available capacity.
- **BR-06**: Every confirmed booking receives a unique ID tracked in a set.
- **BR-07 & BR-08**: Total fare is calculated as `ticket_price × seats`; state changes occur only after all validations pass.
- **BR-09 & BR-10**: Only `Confirmed` bookings can be cancelled; seat capacity is restored exactly once.
- **BR-11 & BR-12**: Cancelled bookings remain in history; cancelled ticket fares are strictly excluded from confirmed revenue calculations.
- **BR-14**: Out-of-range menu inputs are handled cleanly without application crashes.
