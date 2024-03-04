'use strict';

const $cupcakeList = $('#cupcake-list');

async function start() {
  // get the cupcakes and append to cupcake list
  const response = await fetch('/api/cupcakes');

  // {cupcakes: [{}, {}, ...]}
  const cupcake_data = await response.json();
  console.log(cupcake_data)
  for (let c of cupcake_data.cupcakes) {
    $cupcakeList.append($(`<li>
    Flavor: ${c.flavor}
    Size: ${c.size}
    Rating: ${c.rating}
    <img src="${c.image_url}" alt="Photo of a ${c.flavor} cupcake">
    </li>`));
  }
}

start();