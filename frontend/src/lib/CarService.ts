interface Car {
  brand: string;
  make: string;
  year: number;
  price: number;
  km: number;
  cm3: number;
  car_type: string;
  color: string;
}

export async function getCars(): Promise<Car[]> {
  try {
    // const response = await fetch('http://car-store-fasm-dev.ap-southeast-1.elasticbeanstalk.com/cars/');
    const response = await fetch('http://localhost:8000/cars');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const cars: Car[] = await response.json();
     // Optional: Print each car's details
    cars.forEach(car => {
      console.log(`Car: ${car.brand} ${car.make}, Year: ${car.year}, Price: $${car.price}`);
    });
    return cars;
  } catch (error) {
    console.error('Could not fetch cars:', error);
    return [];
  }
}
