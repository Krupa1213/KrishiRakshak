from backend.database import government_schemes_collection
from backend.data.government_schemes import GOVERNMENT_SCHEMES


def seed_government_schemes():
    government_schemes_collection.delete_many({})

    if GOVERNMENT_SCHEMES:
        government_schemes_collection.insert_many(
            GOVERNMENT_SCHEMES
        )

    print(
        f"Inserted {len(GOVERNMENT_SCHEMES)} government schemes successfully!"
    )


if __name__ == "__main__":
    seed_government_schemes()