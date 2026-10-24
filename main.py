"""
Smart Bus Ticket Booking & Reservation System
Product Requirements Document (PRD) Implementation
Language: Python 3 (Standard Built-in Libraries Only)
"""

# ==========================================
# DATA STRUCTURES & INITIALIZATION
# ==========================================

# Feature 2: Store Bus Routes (List of Dictionaries)
routes = [
    {
        "route_id": "R101",
        "departure_city": "Karachi",
        "destination_city": "Hyderabad",
        "departure_time": "08:00 AM",
        "ticket_price": 1200,
        "total_seats": 40,
        "available_seats": 40,
    },
    {
        "route_id": "R102",
        "departure_city": "Karachi",
        "destination_city": "Sukkur",
        "departure_time": "09:30 AM",
        "ticket_price": 2000,
        "total_seats": 36,
        "available_seats": 36,
    },
    {
        "route_id": "R103",
        "departure_city": "Hyderabad",
        "destination_city": "Mirpur Khas",
        "departure_time": "11:00 AM",
        "ticket_price": 800,
        "total_seats": 32,
        "available_seats": 32,
    },
    {
        "route_id": "R104",
        "departure_city": "Karachi",
        "destination_city": "Lahore",
        "departure_time": "07:00 PM",
        "ticket_price": 5000,
        "total_seats": 45,
        "available_seats": 45,
    },
    {
        "route_id": "R105",
        "departure_city": "Sukkur",
        "destination_city": "Hyderabad",
        "departure_time": "02:00 PM",
        "ticket_price": 1500,
        "total_seats": 30,
        "available_seats": 30,
    },
]

# Supported cities collection (Tuple)
supported_cities = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")

# Bookings dataset (List of Dictionaries)
bookings = []

# Set tracking issued booking IDs to guarantee uniqueness (BR-06)
issued_booking_ids = set()

# Counter for sequential booking ID generation
booking_id_counter = 1001


# ==========================================
# HELPER FUNCTIONS & VALIDATORS
# ==========================================

def validate_name(name_input):
    """
    Validates passenger name input.

    • What it does: Checks if the input name is non-empty and contains non-whitespace characters (BR-01).
    
    • returns: True if valid non-blank string, False otherwise.
    """
    if not name_input or not name_input.strip():
        return False
    return True


def validate_positive_int(val_input):
    """
    Validates integer inputs for age and seat quantity.

    • What it does: Converts input string to integer and verifies it is strictly positive (> 0) (BR-02, BR-04).
    
    • returns: Positive integer if valid, None if invalid or non-numeric.
    """
    try:
        val = int(val_input)
        return val if val > 0 else None
    except ValueError:
        return None


def generate_unique_booking_id():
    """
    Generates unique sequential booking IDs.

    • What it does: Creates candidate booking IDs (e.g., 'B1001') and validates against issued_booking_ids set to ensure uniqueness (BR-06).
    
    • returns: Unique booking ID string (e.g., 'B1001').
    """
    global booking_id_counter
    while True:
        candidate_id = f"B{booking_id_counter}"
        booking_id_counter += 1
        if candidate_id not in issued_booking_ids:
            issued_booking_ids.add(candidate_id)
            return candidate_id


def find_route_by_id(route_id):
    """
    Looks up a route by its ID.

    • What it does: Searches the routes dataset case-insensitively for a matching route ID (BR-03).

    • returns: Matching route dictionary if found, None otherwise.
    """
    for r in routes:
        if r["route_id"].upper() == route_id.strip().upper():
            return r
    return None


# ==========================================
# CORE FEATURE FUNCTIONS
# ==========================================

def view_available_routes(filter_available_only=False):
    """
    Displays bus routes and seat availability.

    • What it does: Iterates through routes using enumerate(), formats table output, and optionally filters out fully booked routes.

    • returns: None (prints route details directly to stdout).
    """
    print("")
    print("=" * 70)
    print("AVAILABLE BUS ROUTES")
    print("=" * 70)
    print(f"{'No.':<4} {'Route':<7} {'Journey':<28} {'Depart':<10} {'Fare':<10} {'Seats'}")
    print("-" * 70)

    displayed_count = 0
    for idx, r in enumerate(routes, start=1):
        # BR-13 / Feature 3: use continue to skip fully booked routes when filtering
        if filter_available_only and r["available_seats"] == 0:
            continue

        displayed_count += 1
        journey = f"{r['departure_city']} -> {r['destination_city']}"
        fare_str = f"Rs.{r['ticket_price']}"
        seats_str = (
            "Fully Booked"
            if r["available_seats"] == 0
            else f"{r['available_seats']}/{r['total_seats']}"
        )

        print(
            f"{idx:<4} {r['route_id']:<7} {journey:<28} {r['departure_time']:<10} {fare_str:<10} {seats_str}"
        )

    if displayed_count == 0:
        print("No routes available matching the selection.")
    print("=" * 70)


def search_routes(query_text=None):
    """
    Searches for routes by ID or city name.

    • What it does: Normalizes query string using lower() and searches route IDs and cities using a for-else loop to display matches or a no-match notice.
    
    • returns: None (prints matching routes directly to stdout).
    """
    print("")
    print("--- SEARCH FOR A ROUTE ---")
    if query_text is None:
        query = input("Enter Route ID or City Name to search: ").strip()
    else:
        query = query_text.strip()

    if not query:
        print("[Error] Search query cannot be empty.")
        return

    query_norm = query.lower()
    matches_found = False

    print("")
    print("Matching Routes:")
    print("-" * 65)
    for r in routes:
        # Match route ID, departure city, or destination city
        if (
            query_norm == r["route_id"].lower()
            or query_norm in r["departure_city"].lower()
            or query_norm in r["destination_city"].lower()
        ):
            journey = f"{r['departure_city']} -> {r['destination_city']}"
            print(
                f"{r['route_id']} | {journey} | Rs. {r['ticket_price']} | {r['available_seats']} seats available"
            )
            matches_found = True
    else:
        # for-else block triggers when loop completes
        if not matches_found:
            print(f"No matching routes found for '{query}'.")
    print("-" * 65)


def book_ticket():
    """
    Handles passenger ticket booking transaction.

    • What it does: Collects and validates passenger name, age, route ID, and seat count (BR-01 to BR-05), generates a unique booking ID, calculates fare, creates a booking record, and decrements available seats.
    
    • returns: None (updates global bookings/routes state and prints confirmation or error).
    """
    print("")
    print("--- BOOK A TICKET ---")

    # BR-01: Passenger Name
    passenger_name = input("Enter Passenger Name: ").strip()
    if not validate_name(passenger_name):
        print("[Validation Error] Passenger name cannot be empty or blank. Booking cancelled.")
        return

    # BR-02: Passenger Age
    age_str = input("Enter Passenger Age: ").strip()
    passenger_age = validate_positive_int(age_str)
    if passenger_age is None:
        print("[Validation Error] Age must be a positive integer. Booking cancelled.")
        return

    # BR-03: Route ID Verification
    route_id_input = input("Enter Route ID (e.g., R101): ").strip()
    target_route = find_route_by_id(route_id_input)
    if not target_route:
        print(f"[Validation Error] Route '{route_id_input}' does not exist. Booking cancelled.")
        return

    # BR-04: Seat Quantity Verification
    seats_str = input("Enter Number of Seats: ").strip()
    requested_seats = validate_positive_int(seats_str)
    if requested_seats is None:
        print("[Validation Error] Seat quantity must be a positive integer. Booking cancelled.")
        return

    # BR-05: Seat Availability Check
    if requested_seats > target_route["available_seats"]:
        print(
            f"[Validation Error] Requested seats ({requested_seats}) exceed available seats ({target_route['available_seats']}). Booking cancelled."
        )
        return

    # BR-06: Unique Booking ID Generation
    new_booking_id = generate_unique_booking_id()

    # BR-07: Fare Calculation
    total_fare = target_route["ticket_price"] * requested_seats

    # BR-08: State Change (create booking record and decrement seats)
    booking_record = {
        "booking_id": new_booking_id,
        "passenger_name": passenger_name,
        "passenger_age": passenger_age,
        "route_id": target_route["route_id"],
        "seats": requested_seats,
        "total_fare": total_fare,
        "status": "Confirmed",
    }
    bookings.append(booking_record)
    target_route["available_seats"] -= requested_seats

    # Print Confirmation Output
    print("")
    print("*" * 45)
    print("Booking confirmed!")
    print(f"Booking ID   : {new_booking_id}")
    print(f"Passenger    : {passenger_name} (Age: {passenger_age})")
    print(f"Route        : {target_route['route_id']} ({target_route['departure_city']} -> {target_route['destination_city']})")
    print(f"Seats booked : {requested_seats}")
    print(f"Fare per seat: Rs. {target_route['ticket_price']}")
    print(f"Total fare   : Rs. {total_fare}")
    print("Status       : Confirmed")
    print("*" * 45)


def view_my_bookings():
    """
    Displays all passenger booking history.

    • What it does: Lists all booking records (both Confirmed and Cancelled) with details using enumerate(), or handles empty list cleanly (BR-15).
    
    • returns: None (prints booking records directly to stdout).
    """
    print("")
    print("=" * 80)
    print("BOOKING HISTORY & RECORDS")
    print("=" * 80)

    # BR-15: Handle empty list cleanly
    if not bookings:
        print("No bookings found.")
        print("=" * 80)
        return

    print(
        f"{'No.':<4} {'Booking ID':<12} {'Passenger':<18} {'Route':<8} {'Seats':<7} {'Total Fare':<12} {'Status'}"
    )
    print("-" * 80)

    for idx, b in enumerate(bookings, start=1):
        print(
            f"{idx:<4} {b['booking_id']:<12} {b['passenger_name']:<18} {b['route_id']:<8} {b['seats']:<7} Rs.{b['total_fare']:<9} {b['status']}"
        )

    print("=" * 80)


def cancel_booking():
    """
    Cancels a confirmed booking and restores route seats.

    • What it does: Validates booking ID, verifies status is Confirmed (BR-09), updates status to Cancelled (BR-11), and restores seat count to the route exactly once (BR-10).
   
    • returns: None (updates booking/route state and prints cancellation details or error).
    """
    print("")
    print("--- CANCEL A BOOKING ---")

    if not bookings:
        print("No bookings currently exist to cancel.")
        return

    booking_id_input = input("Enter booking ID to cancel: ").strip().upper()

    # Locate booking using loop
    target_booking = None
    for b in bookings:
        if b["booking_id"].upper() == booking_id_input:
            target_booking = b
            break

    if not target_booking:
        print(f"[Error] Booking ID '{booking_id_input}' not found.")
        return

    # BR-09: Reject if already cancelled
    if target_booking["status"] == "Cancelled":
        print(f"[Error] Booking '{booking_id_input}' is already Cancelled. Cannot cancel again.")
        return

    # Locate route to restore seats
    route = find_route_by_id(target_booking["route_id"])
    if route:
        # BR-10: Restore seats exactly once
        route["available_seats"] += target_booking["seats"]
        restored_seats = target_booking["seats"]
        current_avail = route["available_seats"]
    else:
        restored_seats = target_booking["seats"]
        current_avail = "N/A"

    # BR-11: Retain record and update status
    target_booking["status"] = "Cancelled"

    print("")
    print("-" * 45)
    print(f"Booking {target_booking['booking_id']} has been cancelled.")
    print(f"Seats restored: {restored_seats}")
    print(f"Route {target_booking['route_id']} available seats: {current_avail}")
    print("-" * 45)


def view_seat_availability():
    """
    Displays capacity and availability status for all routes.

    • What it does: Compares available seats against total seats for each route and classifies status as Available, Partially Booked, or Fully Booked.
    
    • returns: None (prints seat status table directly to stdout).
    """
    print("")
    print("=" * 65)
    print("SEAT AVAILABILITY & CAPACITY STATUS")
    print("=" * 65)
    print(f"{'Route ID':<10} {'Journey':<28} {'Capacity':<12} {'Status'}")
    print("-" * 65)

    for r in routes:
        journey = f"{r['departure_city']} -> {r['destination_city']}"
        cap_str = f"{r['available_seats']} / {r['total_seats']}"

        if r["available_seats"] == r["total_seats"]:
            status = "Available"
        elif r["available_seats"] == 0:
            status = "Fully Booked"
        else:
            status = "Partially Booked"

        print(f"{r['route_id']:<10} {journey:<28} {cap_str:<12} {status}")

    print("=" * 65)


def view_route_schedules():
    """
    Displays route departure schedules grouped by city.

    • What it does: Uses nested for loops (outer loop over supported_cities tuple, inner loop over routes) to display scheduled departures by departure city.
    
    • returns: None (prints departure schedules directly to stdout).
    """
    print("")
    print("=" * 60)
    print("ROUTE SCHEDULE BY DEPARTURE CITY")
    print("=" * 60)

    # Outer loop over supported_cities tuple
    for city in supported_cities:
        print(f"\n{city}")
        departures_found = False

        # Inner loop over routes list
        for r in routes:
            if r["departure_city"].lower() == city.lower():
                print(f"   {r['route_id']} -> {r['destination_city']:<15} | {r['departure_time']}")
                departures_found = True

        if not departures_found:
            print("   No scheduled departures.")

    print("\n" + "=" * 60)


def generate_booking_report():
    """
    Generates system metrics and financial analytics report.

    • What it does: Calculates total bookings, confirmed count, cancelled count, reserved seats, confirmed revenue (excluding cancelled fares per BR-12), and fully booked route count.
    
    • returns: None (prints summary report directly to stdout).
    """
    print("")
    print("=" * 55)
    print("BOOKING REPORT & SYSTEM ANALYTICS")
    print("=" * 55)

    total_created = len(bookings)
    confirmed_count = 0
    cancelled_count = 0
    reserved_seats = 0
    confirmed_revenue = 0

    # Process booking statistics
    for b in bookings:
        if b["status"] == "Confirmed":
            confirmed_count += 1
            reserved_seats += b["seats"]
            confirmed_revenue += b["total_fare"]  # BR-12
        elif b["status"] == "Cancelled":
            cancelled_count += 1

    # Calculate fully booked routes count
    fully_booked_routes_count = 0
    for r in routes:
        if r["available_seats"] == 0:
            fully_booked_routes_count += 1

    print(f"Total bookings created  : {total_created}")
    print(f"Confirmed bookings      : {confirmed_count}")
    print(f"Cancelled bookings      : {cancelled_count}")
    print(f"Seats currently reserved: {reserved_seats}")
    print(f"Confirmed revenue       : Rs. {confirmed_revenue:,}")
    print(f"Fully booked routes     : {fully_booked_routes_count}")
    print("=" * 55)


# ==========================================
# MAIN APPLICATION LOOP
# ==========================================

def main():
    """
    Runs main application menu and execution loop.

    • What it does: Displays 9-option interactive console menu, routes user choices to corresponding feature functions, and handles invalid inputs gracefully without crashing (BR-14).
    
    • returns: None (executes continuously until option 9 is selected).
    """
    while True:
        print("")
        print("=" * 40)
        print("   SMART BUS RESERVATION SYSTEM")
        print("=" * 40)
        print("1. View Available Routes")
        print("2. Search for a Route")
        print("3. Book a Ticket")
        print("4. View My Bookings")
        print("5. Cancel a Booking")
        print("6. View Seat Availability")
        print("7. View Route Schedules")
        print("8. Generate Booking Report")
        print("9. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            view_available_routes()
        elif choice == "2":
            search_routes()
        elif choice == "3":
            book_ticket()
        elif choice == "4":
            view_my_bookings()
        elif choice == "5":
            cancel_booking()
        elif choice == "6":
            view_seat_availability()
        elif choice == "7":
            view_route_schedules()
        elif choice == "8":
            generate_booking_report()
        elif choice == "9":
            print("")
            print("Thank you for using the Smart Bus Reservation System. Goodbye!")
            break
        else:
            # BR-14: Handle non-numeric or out-of-range choices safely
            print("")
            print("[Error] Invalid choice! Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()
