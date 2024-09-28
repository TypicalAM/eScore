API_URL = 'http://localhost:5000';

async function fetchFromAPI() {
	const tabURL = window.location.href;
	console.log('fetching rating for: ', tabURL);

	try {
		const response = await fetch(`${API_URL}/check_url`, {
			method: 'POST',
			mode: 'no-cors',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				url: tabURL
			})
		});

		if (!response.ok) {
			console.log('Failed to fetch rating');
			return 'Failed to fetch rating';
		}
	} catch {
		console.log('Failed to fetch rating');
		return 'Failed to fetch rating';
	};
	
	console.log('fetched from: ', response.url);

	const data = await response.json();
	console.log('received data: ', data);

	return data;
}

(async function() {
	let rating = 'No rating available';
	rating = await fetchFromAPI();

	document.body.innerHTML += '<div id="rating">' + rating + '</div>';
})();
