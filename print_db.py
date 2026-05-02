import sqlite3
import permissions as perms

DB_PATH = "data.db"
db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

permissions = [
    "host"
]

def show_database():
    print("\n" + "=" * 50)
    print("GAME STATE")
    print("=" * 50)
    cursor.execute("SELECT is_running FROM game_state")
    rows = cursor.fetchall()
    if rows:
        print(f"  {'Is Running'}")
        print("  " + "-" * 30)
        for is_running in rows:
            print(f"  {bool(is_running)}")
    else:
        print("  (no entries)")

    print("\n" + "=" * 50)
    print("USER PERMISSIONS")
    print("=" * 50)
    cursor.execute("SELECT user_id, permission FROM user_permissions")
    rows = cursor.fetchall()
    if rows:
        print(f"  {'User ID':<20} {'Permission'}")
        print("  " + "-" * 30)
        for user_id, permission in rows:
            print(f"  {user_id:<20} {permission}")
    else:
        print("  (no entries)")
    print()


def grant_permission_cli():
    show_database()
    print("Grant permission to a user")
    print("-" * 30)
    user_id  = int(input("User ID   : "))
    print(f"Available permissions: {permissions}")
    permission = input("Permission: ").strip()
    if permission not in permissions:
        print(f"Invalid permission '{permission}'. Choose from: {permissions}")
        return
    perms.add_permission(user_id, permission)
    print(f"Granted '{permission}' to user {user_id}")


if __name__ == "__main__":
    grant_permission_cli()