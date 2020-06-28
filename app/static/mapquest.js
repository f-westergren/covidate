window.onload = function() {
  placeSearch({
    key: 'lYrP4vF3Uk5zgTiGGuEzQGwGIVDGuy24',
    container: document.querySelector('#search-input'),
    useDeviceLocation: true,
    collection: [
      'address',
      'adminArea',
    ]
  });
}