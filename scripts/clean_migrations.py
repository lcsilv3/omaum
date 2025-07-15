import os
import shutil
import datetime


def backup_database():
    """Create a backup of the database file if it exists"""
    if os.path.exists("db.sqlite3"):
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(
            backup_dir, f"db_backup_{timestamp}.sqlite3"
        )

        shutil.copy2("db.sqlite3", backup_file)
        print(f"Database backed up to {backup_file}")
    else:
        print("No database file found to backup")


def delete_migrations():
    """Delete all migration files except __init__.py"""
    # Get all directories in the current folder
    dirs = [
        d
        for d in os.listdir(".")
        if os.path.isdir(d)
        and not d.startswith(".")
        and d != "venv"
        and d != "backups"
    ]

    migration_files_deleted = 0

    for app_dir in dirs:
        migrations_dir = os.path.join(app_dir, "migrations")
        if os.path.exists(migrations_dir):
            print(f"Checking migrations in {app_dir}...")

            # Get all Python files in the migrations directory
            migration_files = [
                f
                for f in os.listdir(migrations_dir)
                if f.endswith(".py") and f != "__init__.py"
            ]

            # Delete each migration file
            for migration_file in migration_files:
                file_path = os.path.join(migrations_dir, migration_file)
                os.remove(file_path)
                print(f"  Deleted: {file_path}")
                migration_files_deleted += 1

            # Make sure __init__.py exists
            init_file = os.path.join(migrations_dir, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w"):
                    pass  # Create an empty file
                print(f"  Created: {init_file}")

    return migration_files_deleted


def delete_database():
    """Delete the SQLite database file"""
    if os.path.exists("db.sqlite3"):
        os.remove("db.sqlite3")
        print("Database file deleted: db.sqlite3")
        return True
    else:
        print("No database file found to delete")
        return False


def main():
    print("Django Migration Cleaner")
    print("=======================")

    # Ask for confirmation
    confirm = input(
        "This will delete all migration files and the database. Continue? (y/n): "
    )
    if confirm.lower() != "y":
        print("Operation cancelled.")
        return

    # Ask about backup
    backup = input("Create a backup of the database before deleting? (y/n): ")
    if backup.lower() == "y":
        backup_database()

    # Delete migrations
    migration_count = delete_migrations()
    print(f"Deleted {migration_count} migration files")

    # Delete database
    delete_database()

    print("\nCleanup complete!")
    print("Next steps:")
    print("1. Run: python manage.py makemigrations")
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py createsuperuser")
    print("4. Run: python popular_alunos.py (if you want sample data)")


if __name__ == "__main__":
    main()
