// // Do this first
// function getData(){
//     fetch('http://localhost:5000/get_data')
//         .then( response => response.json() )
//         .then( data => console.log(data))
// }

// function getPokemonNames(){
//     fetch('https://pokeapi.co/api/v2/pokemon-species/1/')
//     .then( response => response.json() )
//     .then( data => console.log(data))
// }

// // Prints out { message : "Hello World" }
// getData();

document.getElementById("pokemon-species").addEventListener("change", function() {
    var selectedOption = this.options[this.selectedIndex];
    var selectedPokemonName = selectedOption.value.toLowerCase();
    console.log(selectedOption, selectedPokemonName)
    // Construct the query URL for the Pokémon sprite based on its name
    var spriteQueryUrl = "https://pokeapi.co/api/v2/pokemon/" + selectedPokemonName + "/";

    // Fetch the sprite URL using the query URL
    fetch(spriteQueryUrl)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Extract the sprite URL from the data
            var spriteUrl = data.sprites.front_default;

            // Set the sprite URL as the value of the hidden input field
            document.getElementById("sprite-url").value = spriteUrl;
            console.log("sprite URL is", spriteUrl)
        })
        .catch(function(error) {
            console.log("Error fetching sprite:", error);
        });
});