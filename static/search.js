// global currentUser variable
let currentSearch = null
let chart = null
let showAll = false

async function processForm(e) {
  e.preventDefault()
  const location = document.querySelector('#search-input').value
  const date = document.querySelector('#date').value

  try {
  const searchInstance = await Search.create(location, date)
  currentSearch = searchInstance
  } catch (e) {
    console.log(e)
  }

  chart = currentSearch.generateGraph('#cases-chart')
  document.querySelector('#show-btn').classList.remove('d-none')
}

document.querySelector('#search-form').addEventListener("submit", processForm)

document.querySelector('#show-btn').addEventListener('click', (e) => {
  if (!showAll) {
    currentSearch.showAllDates(chart)
    e.target.classList.remove('btn-primary')
    e.target.classList.add('btn-outline-primary')
  } else {
    currentSearch.generateGraph('#cases-chart')
    e.target.classList.remove('btn-outline-primary')
    e.target.classList.add('btn-primary')
  }
  showAll = !showAll
})

document.querySelector('#death-btn').addEventListener('click', () => {
  chart.load({
    columns: [
        ['deaths', ...currentSearch.deaths]
    ]
});
})
