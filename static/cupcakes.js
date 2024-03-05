'use strict';

const $cupcakeList = $('#cupcake-list');
const $newCupcakeButton = $('#add-cupcake-btn');
const $cupcakeForm = $('#new-cupcake-form');
const BASE_URL = '/api/cupcakes';

$newCupcakeButton.on('click', handleNewCupcakeSubmit);

/** Makes fetch request to add new cupcake to db. Adds new cupcake to DOM. */
async function handleNewCupcakeSubmit(evt) {
  evt.preventDefault();
  const response = await fetch(
    BASE_URL,
    {
      method: "POST",
      body: JSON.stringify({
        flavor: $('#flavor').val(),
        size: $('#size').val(),
        rating: $('#rating').val(),
        image_url: $('#image_url').val()
      }),
      headers: {
        "Content-Type": "application/json"
      },
    }
  );

  const cupcakeData = await response.json();

  appendCupcake(cupcakeData.cupcake);

  $cupcakeForm.trigger('reset');

}

/** Fetches cupcakes data and displays in DOM. */
async function start() {
  // get the cupcakes and append to cupcake list
  const response = await fetch(BASE_URL);

  // {cupcakes: [{}, {}, ...]}
  const cupcakeData = await response.json();
  for (let c of cupcakeData.cupcakes) {
    appendCupcake(c);
  }
}

/** Append cupcake object {flavor, size, rating, image_url}
 * to cupcake list DOM element. */
function appendCupcake(cupcake) {
  $cupcakeList.append($(`<li>
    Flavor: ${cupcake.flavor}
    Size: ${cupcake.size}
    Rating: ${cupcake.rating}
    <img src="${cupcake.image_url}" alt="Photo of a ${cupcake.flavor} cupcake">
    </li>`));
}

start();