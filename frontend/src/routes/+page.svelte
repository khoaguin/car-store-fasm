<script>
	import { getCars } from '../lib/CarService';
	import { onMount } from 'svelte';

	let cars = [];

	onMount(async () => {
		cars = await getCars();
	});
</script>

<main>
	<h1>Welcome to DKAI Car Selling Store</h1>
	<h2>Here are the some cars we have in store</h2>
	{#if cars.length > 0}
		<ul>
			{#each cars as car}
				<li>
					{car.brand}
					{car.make} - Car Type: {car.car_type}, Year: {car.year}, Price: ${car.price}, Km: {car.km},
					Volume: {car.cm3} cm3, Color: {car.color}
				</li>
			{/each}
		</ul>
	{:else}
		<p>Loading cars...</p>
	{/if}
</main>
