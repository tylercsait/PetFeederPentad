import pets
from datetime import date, datetime

todaydate = date.today().isoformat()

# Example usage
pets.add_pet("69", 1, 1)
pets.add_pet("12", 2, 1)
pets.update_pet_feedings_today("69", todaydate)
print(pets.check_pet_exists("12"))
#delete_pet("69", todaydate)
pets.list_all_pets()
pets.delete_all_pets()