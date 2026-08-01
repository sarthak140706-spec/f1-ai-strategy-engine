"""
Sprint 6 - Step 1
Full-Grid Driver Discovery Test
"""

from src.data_loader import load_session
from src.strategy.grid_manager import discover_drivers


SEASON = 2025
GRAND_PRIX = "British Grand Prix"
SESSION_TYPE = "R"


print("=" * 80)
print(
    "V5 SPRINT 6 - STEP 1"
)
print(
    "FULL-GRID DRIVER DISCOVERY VALIDATION"
)
print("=" * 80)

print(
    f"Season: {SEASON}"
)

print(
    f"Grand Prix: {GRAND_PRIX}"
)

print(
    f"Session: {SESSION_TYPE}"
)

print("=" * 80)


# --------------------------------------------------
# LOAD SESSION
# --------------------------------------------------

print(
    "\n[1/3] Loading FastF1 session..."
)

try:

    session = load_session(

        SEASON,

        GRAND_PRIX,

        SESSION_TYPE

    )

    print(
        "FastF1 session loaded successfully."
    )

except Exception as e:

    print(
        f"❌ FAIL - Could not load session."
    )

    print(
        f"Error: {type(e).__name__}: {e}"
    )

    raise SystemExit(
        1
    )


# --------------------------------------------------
# DISCOVER DRIVERS
# --------------------------------------------------

print(
    "\n[2/3] Discovering all participating drivers..."
)

try:

    drivers = discover_drivers(
        session
    )

    print(
        f"Discovered {len(drivers)} drivers."
    )

except Exception as e:

    print(
        "❌ FAIL - Driver discovery failed."
    )

    print(
        f"Error: {type(e).__name__}: {e}"
    )

    raise SystemExit(
        1
    )


# --------------------------------------------------
# DISPLAY GRID
# --------------------------------------------------

print(
    "\n[3/3] Full-grid driver list..."
)

print(
    "-" * 80
)

for index, driver in enumerate(
    drivers,
    start=1
):

    print(

        f"{index:2d}. "

        f"{driver['driver']:>3} | "

        f"Number: "
        f"{str(driver['driver_number']):>3} | "

        f"Position: "
        f"{str(driver['position']):>2} | "

        f"Name: "
        f"{driver['name']} | "

        f"Team: "
        f"{driver['team']}"

    )

print(
    "-" * 80
)


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

if len(drivers) < 2:

    print(
        "\n❌ STEP 1 FAILED"
    )

    print(
        "Fewer than 2 drivers were discovered."
    )

    raise SystemExit(
        1
    )


print(
    "\n✅ STEP 1 - FULL-GRID DRIVER DISCOVERY PASSED"
)

print(
    f"Total drivers discovered: {len(drivers)}"
)

print(
    "Dynamic driver discovery is working successfully."
)