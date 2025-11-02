from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from datetime import datetime
import sys

async def seed_database():
    client = None
    try:
        print("\n=== Database Seeding Tool ===\n")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client.diabetes_db
        
        # Verify connection
        await client.admin.command('ping')
        print("✓ Connected to MongoDB\n")

        # Sample patient data
        sample_patients = [
            {
                "PatientID": 1001,
                "Age": 45,
                "Sex": 1,
                "BMI": 28.5,
                "HighBP": True,
                "HighChol": True,
                "CholCheck": True,
                "Smoker": False,
                "Stroke": False,
                "HeartDiseaseorAttack": False,
                "PhysActivity": True,
                "Fruits": True,
                "Veggies": True,
                "HvyAlcoholConsump": False,
                "AnyHealthcare": True,
                "NoDocbcCost": False,
                "GenHlth": 2,
                "MentHlth": 0,
                "PhysHlth": 0,
                "DiffWalk": False,
                "Education": 4,
                "Income": 6,
                "created_at": datetime.now()
            },
            {
                "PatientID": 1002,
                "Age": 52,
                "Sex": 0,
                "BMI": 32.1,
                "HighBP": True,
                "HighChol": True,
                "CholCheck": True,
                "Smoker": True,
                "Stroke": False,
                "HeartDiseaseorAttack": True,
                "PhysActivity": False,
                "Fruits": False,
                "Veggies": True,
                "HvyAlcoholConsump": False,
                "AnyHealthcare": True,
                "NoDocbcCost": False,
                "GenHlth": 3,
                "MentHlth": 5,
                "PhysHlth": 10,
                "DiffWalk": True,
                "Education": 3,
                "Income": 4,
                "created_at": datetime.now()
            }
        ]

        print("Clearing existing data...")
        await db.patients.delete_many({})
        await db.health_conditions.delete_many({})
        await db.lifestyle_factors.delete_many({})
        await db.health_metrics.delete_many({})
        await db.healthcare_access.delete_many({})

        print("Inserting sample patients...")
        for patient in sample_patients:
            # Insert base patient data
            await db.patients.insert_one({
                "PatientID": patient["PatientID"],
                "Age": patient["Age"],
                "Sex": patient["Sex"],
                "Education": patient["Education"],
                "Income": patient["Income"],
                "created_at": patient["created_at"]
            })

            await db.health_conditions.insert_one({
                "PatientID": patient["PatientID"],
                "HighBP": patient["HighBP"],
                "HighChol": patient["HighChol"],
                "Stroke": patient["Stroke"],
                "HeartDiseaseorAttack": patient["HeartDiseaseorAttack"]
            })

            await db.lifestyle_factors.insert_one({
                "PatientID": patient["PatientID"],
                "BMI": patient["BMI"],
                "Smoker": patient["Smoker"],
                "PhysActivity": patient["PhysActivity"],
                "Fruits": patient["Fruits"],
                "Veggies": patient["Veggies"],
                "HvyAlcoholConsump": patient["HvyAlcoholConsump"]
            })

            await db.health_metrics.insert_one({
                "PatientID": patient["PatientID"],
                "CholCheck": patient["CholCheck"],
                "GenHlth": patient["GenHlth"],
                "MentHlth": patient["MentHlth"],
                "PhysHlth": patient["PhysHlth"],
                "DiffWalk": patient["DiffWalk"]
            })

            await db.healthcare_access.insert_one({
                "PatientID": patient["PatientID"],
                "AnyHealthcare": patient["AnyHealthcare"],
                "NoDocbcCost": patient["NoDocbcCost"]
            })

        print("\n✓ Database seeded successfully!")
        print(f"✓ Added {len(sample_patients)} sample patients")
        print("✓ Created all required collections")

    except Exception as e:
        print(f"\n Error: {str(e)}")
        sys.exit(1)
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())