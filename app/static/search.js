async function processForm(e) {
  e.preventDefault()
  const location = document.querySelector('#search-input').value
  const date = document.querySelector('#date').value
  console.log(location, date)
  try {
    res = await axios.post('http://localhost:5000/search', {
      "location": location,
      "date": date
  })

  console.log(res)
  } catch (err) {
    console.log(err)
  }
}

document.querySelector('#search-form').addEventListener("submit", processForm)