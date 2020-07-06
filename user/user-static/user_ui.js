// global currentSearch variable
const loader = document.querySelector('#loader')
const toggleBtn = document.querySelector('#toggle-btn')
const dateBtn = document.querySelector('#date-btn')
const deleteBtn = document.querySelector('#delete-btn')
const message = document.querySelector('#message')
const searchHeader = document.querySelector('#search-heading')
const searchSubtitle = document.querySelector('#search-subtitle')

let savedSearch = null
let chart = null
let showLoader = false
let showDates = false

async function loadSearch(e) {
  e.preventDefault()
  document.querySelector('#loader').classList.remove('d-none')
  try {
    const response = await Search.load(e.target.id)
    savedSearch = response

    // Render chart from results
    chart = savedSearch.generateChart('#cases-chart')
  
    // Show buttons
    toggleBtn.classList.remove('d-none')
    dateBtn.classList.remove('d-none')
    deleteBtn.classList.remove('d-none')

    // Show title
    searchHeader.innerText = `${savedSearch.location}`
    searchSubtitle.innerText = `(created at: ${savedSearch.created_at})`

    searchHeader.classList.remove('d-none')
    searchSubtitle.classList.remove('d-none')
  
    // Hide and update error divs and buttons.
    message.classList.add('d-none')
    message.innerText = ''
    loader.classList.add('d-none')
  
    } catch (err) {
      loader.classList.add('d-none')
      message.classList.remove('d-none')
      message.innerText = "Can't load search."
    }
    
  chart = savedSearch.generateChart('#cases-chart')
}

// Toggle between showing 15 days from search date or all days until search creation
const toggleAllDates = (e) => {
  if (!showDates) {
    savedSearch.showAllDates(chart)
    e.target.innerText = 'Show 15 Days'
    showDates = true
  } else {
    savedSearch.showFifteenDates(chart)
    e.target.innerText = 'Show Until Today'
    showDates = false
  }
}

// Toggle between showing deaths and showing cases 
const toggleDeaths = (e) => {
  let legend = document.querySelector('.c3-legend-item').textContent
  if (legend == 'deaths') {
    savedSearch.showCases(showDates)
    e.target.innerText = 'Show Deaths'
  } else {
    savedSearch.showDeaths(showDates)
    e.target.innerText = 'Show Cases'
  }
}

async function deleteSearch(e) {
  e.preventDefault()
  try { 
    response = await savedSearch.delete()
    if (response === 'deleted') {
      message.innerText="Search deleted."
      message.classList.remove('d-none')
    } else {
      message.innerText="Can't delete search right now."
      message.classList.remove('d-none')
    }
  } catch (err) {
    message.innerText="Can't delete search."
  }
}

document.querySelector('#saved-search').addEventListener('click', loadSearch)
dateBtn.addEventListener('click', (e) => toggleAllDates(e))
toggleBtn.addEventListener('click', (e) => toggleDeaths(e))
deleteBtn.addEventListener('click', deleteSearch)


