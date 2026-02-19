import asyncio
import os
from dotenv import load_dotenv
from backend.db.mongo import mongo
from backend.db.indexes import ensure_indexes
from backend.routers.users import (
    create_user,
    get_user,
    get_users,
    update_user,
    patch_user,
    delete_user
)
from backend.models.user import UserProfile, UserProfileUpdate

# Load environment variables
load_dotenv()


async def main():
    """Main test function - runs all CRUD operations"""

    print("\n" + "=" * 60)
    print("MONGODB USER CRUD TESTING (Using FastAPI Routers)")
    print("=" * 60 + "\n")

    # Connect to test database
    test_db = os.getenv("TEST_DB")
    print(f"Connecting to test database: {test_db}")
    await mongo.connect(test_db)
    await ensure_indexes()
    print(" Connected to MongoDB\n")

    test_user_id = None

    try:
        # ============================================================
        # TEST 1: CREATE USER
        # ============================================================
        print("=" * 60)
        print("TEST 1: CREATE USER")
        print("=" * 60)

        new_user = UserProfile(
            name="Pref User",
            email="pref@test.com",
            preferences={
                "desired_locations": ["NYC", "SF"],
                "target_roles": ["ML Engineer"],
                "skills": ["Python", "FastAPI"],
                "experience_level": "mid",
                "salary_min": 90000,
                "salary_max": 130000
            }
        )

        created_user = await create_user(new_user)
        test_user_id = created_user['id']

        print("User created:")
        print(f"  ID: {test_user_id}")
        print(f"  Name: {created_user['name']}")
        print(f"  Email: {created_user['email']}")
        print(f"  Preferences: {created_user['preferences']}\n")

        # ============================================================
        # TEST 2: GET SINGLE USER
        # ============================================================
        print("=" * 60)
        print("TEST 2: GET USER")
        print("=" * 60)

        retrieved_user = await get_user(test_user_id)
        print(" User retrieved:")
        print(f"  ID: {retrieved_user['id']}")
        print(f"  Name: {retrieved_user['name']}")
        print(f"  Email: {retrieved_user['email']}")
        print(f"  Preferences: {retrieved_user['preferences']}\n")

        # ============================================================
        # TEST 3: UPDATE USER (PUT)
        # ============================================================
        print("=" * 60)
        print("TEST 3: PUT USER (Full Update)")
        print("=" * 60)

        user_updates = UserProfileUpdate(
            name="Updated Pref User",
            preferences={
                "skills": ["Java"],
                "experience_level": "junior",
                "salary_min": 80000,
            }
        )

        updated_user = await update_user(test_user_id, user_updates)
        print(" User updated:")
        print(f"  Skills: {', '.join(updated_user['preferences'].get('skills', []))}")
        print(f"  Experience: {updated_user['preferences'].get('experience_level', 'N/A')}")
        print(f"  Min Salary: ${updated_user['preferences'].get('salary_min', 'N/A')}\n")

        # ============================================================
        # TEST 4: PATCH USER (Partial Update)
        # ============================================================
        print("=" * 60)
        print("TEST 4: PATCH USER (Partial Update)")
        print("=" * 60)

        partial_updates = UserProfileUpdate(
            name="Updated",
            preferences={
                "desired_locations": ["New York", "Remote", "Boston"]
            }
        )

        patched_user = await patch_user(test_user_id, partial_updates)
        print(" User patched:")
        print(f"  Name: {patched_user['name']}")
        print(f"  Locations: {', '.join(patched_user['preferences'].get('desired_locations', []))}")
        print(f"  Skills (unchanged): {', '.join(patched_user['preferences'].get('skills', []))}\n")

        # ============================================================
        # TEST 5: GET ALL USERS
        # ============================================================
        print("=" * 60)
        print("TEST 5: GET ALL USERS")
        print("=" * 60)

        all_users = await get_users()
        print(f" Found {len(all_users)} user(s):")
        for user in all_users:
            print(f"  - {user['email']} (ID: {user['id']})")
        print()

        # ============================================================
        # TEST 6: DELETE USER
        # ============================================================
        print("=" * 60)
        print("TEST 6: DELETE USER (with cascading)")
        print("=" * 60)

        await delete_user(test_user_id)
        print(f" User deleted (ID: {test_user_id})")

        # Verify deletion
        try:
            await get_user(test_user_id)
            print(" User still exists!\n")
        except Exception as e:
            print(" User successfully deleted (confirmed): ", e)

        # ============================================================
        # ALL TESTS COMPLETE
        # ============================================================
        print("=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except Exception as e:
        print(f"\n Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        # Close MongoDB connection
        await mongo.close()
        print("\n MongoDB connection closed\n")


if __name__ == "__main__":
    asyncio.run(main())
