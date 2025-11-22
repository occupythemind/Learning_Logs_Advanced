let origin = window.location.origin

async function showNotification(message, type = 'error', duration = 3000) {
  const popup = document.getElementById('notification-popup');
  const msgEl = document.getElementById('notification-message');

  // Reset previous types
  popup.classList.remove('error', 'success', 'info');

  // Set new type
  popup.classList.add(type);

  // Set message
  msgEl.textContent = message;

  // Show popup
  popup.classList.add('show');

  // Hide after duration
  setTimeout(() => {
      popup.classList.remove('show');
  }, duration);
};


function redirectToUrl(button, target='_blank') {
    var url = button.getAttribute('data-url');
    // Change the URL on the current tab
    // NOTE: Only use remain for on site URLs and not external URLs
    if (target.trim() == 'remain') {
        window.location.href = url;
    } else { // Open a new tab (default)
        window.open(url, '_blank', 'noopener,noreferrer'); // For security reasons 😅, OKAY & UX
    }
};


function get_pk_fromurlend() {
  // captures the pk from the end of the url and returns it.
  const parts = window.location.pathname.split("/").filter(Boolean);
  const pk = parts.pop();
  return pk;
};

// get all data from API and fill a table
async function create_table_data({
  retries = 3,
  baseDelay = 1000,
  endpoint = '/api/topics/',
  t_id = 'table-data',
  excludeKeys = ['id', 'date_added', 'date_modified'],
  sortKey = 'date_modified',
  sortOrder = 'new-old',
  main = 'title', // The main content of the Object returned (dict)
  r_key = 'id', // redirect dict key value (pk for API OBJ ref)
  redirect_to = `${window.origin}/topic/`, // redirect to an entry endpoint, also appending the id of that topic

} = {}) {
  const url = (typeof origin !== 'undefined' ? origin : window.location.origin) + endpoint;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await fetch(url);

      if (!response.ok) {
        if (response.status >= 500) {
          throw new Error(`Server error (HTTP ${response.status})`);
        } else {
          showNotification(`Request failed (HTTP ${response.status}). Please try again later.`);
          return;
        }
      }

      const data = await response.json();
      const table = document.getElementById(t_id);
      table.innerHTML = "";

      if (!Array.isArray(data) || data.length === 0) {
        const msgRow = document.createElement("tr");
        const td = document.createElement("td");
        td.colSpan = 10;
        td.textContent = "No data available.";
        msgRow.appendChild(td);
        table.appendChild(msgRow);
        return;
      }

      // --- Sort by sortKey if provided ---
      if (sortKey && sortKey in data[0]) {
        data.sort((a, b) => {
          const aVal = a[sortKey];
          const bVal = b[sortKey];

          const aTime = new Date(aVal).getTime();
          const bTime = new Date(bVal).getTime();

          return sortOrder === 'old-new' ? aTime - bTime : bTime - aTime;
        });
      }

      // --- Table header ---
      const firstItem = data[0];
      const header = document.createElement("tr");
      for (const key in firstItem) {
        if (excludeKeys.includes(key)) continue;
        const th = document.createElement("th");
        th.textContent = key.charAt(0).toUpperCase() + key.slice(1);
        header.appendChild(th);
      }
      table.appendChild(header);

      // --- Table body ---
      data.forEach(item => {
      const tr = document.createElement("tr");
      for (const key in item) {
        if (excludeKeys.includes(key)) continue;
        const td = document.createElement("td");
        td.textContent = item[key];
        if (r_key in item) {
        td.style.cursor = 'pointer';
        td.style.border = '2px solid black';
        td.style.backgroundColor = 'black';
        td.style.color = 'white';
        var url = redirect_to + item[r_key];
        td.dataset.url = url;
        td.onclick = () => redirectToUrl(td, target='remain');
      }
        tr.appendChild(td);
      }

      table.appendChild(tr);
    });


      return;

    } catch (err) {
      const isNetworkError = err instanceof TypeError;

      if (attempt < retries) {
        const delay = baseDelay * Math.pow(2, attempt - 1);
        const errType = isNetworkError ? "network" : "server";
        showNotification(`Temporary ${errType} issue — retrying (${attempt}/${retries})...`);

        console.warn(`Attempt ${attempt} failed (${errType}): ${err.message}`);
        console.log(`Retrying in ${delay / 1000}s...`);

        await new Promise(res => setTimeout(res, delay));
        continue;
      }

      const finalMessage = isNetworkError
        ? "Network error — please check your connection and try again."
        : "Server is currently unavailable — please try again later.";

      showNotification(finalMessage);
      console.error(`All ${retries} attempts failed:`, err);
    }
  }
};

// QUES:
// In JS, how can I know the total no. of text that can fit in a box?

function changeTagName(el, newTag) {
  // Create a new element with the desired tag
  const newEl = document.createElement(newTag);

  // Copy attributes from the old element
  for (const attr of el.attributes) {
    newEl.setAttribute(attr.name, attr.value);
  }

  // Move over all child nodes (text, elements, etc.)
  while (el.firstChild) {
    newEl.appendChild(el.firstChild);
  }

  // Replace the old element with the new one in the DOM
  el.parentNode.replaceChild(newEl, el);

  return newEl; // return the new element if you need it
};

async function getApiObjectData({endpoint='/api/topics/', pk, key} = {}) {
  // fetch the data and return the key's value
  try {
    const Response = await fetch(endpoint + pk);
    const Data = await Response.json();

    // if key exists return, else return null
    return (Data[key] !== undefined ? Data[key] : null);
  } catch (error) {
    console.log(error);
  }
};

async function fillContent({
  entry_endpoint, topic_endpoint, t_el, e_el, navT_el, navE_el, pageTeller,
  topic_url='/topic/', entry_url='/entry/', entry_pk, topic_pk} = {}){
  // fetch the entry object, then get the topic id and fetch the topic object
  // fills both the entry and topic
  // t_el (Topic element); e_el (Entry Element); navT_el (navbar Topic Element); 
  // navE_el (navbar Entry Element); pageTeller (The box that allows adding of these 2 navs above)
  try {
    let text = await getApiObjectData({endpoint: entry_endpoint, pk: entry_pk, key: 'text'});
    if (e_el !== undefined) e_el.textContent = text; // fill entry body
    if (navE_el !== undefined) navE_el.textContent = ' > ' + text; // fill navbar entry

    let title = await getApiObjectData({endpoint: topic_endpoint, pk: topic_pk, key: 'title'});
    if (navT_el !== undefined) navT_el.textContent = ' > ' + title; // fill navbar topic

    navT_el.dataset.url = topic_url + topic_pk;
    navE_el.dataset.url = entry_url + entry_pk;
    navT_el.addEventListener('click', () => redirectToUrl(navT_el, target='remain'));
    navE_el.addEventListener('click', () => redirectToUrl(navE_el, target='remain'));

    navT_el.setAttribute('class', 'truncate-sx');
    navE_el.setAttribute('class', 'truncate-bx');

    if (pageTeller !== undefined){
      pageTeller.appendChild(navT_el);
      pageTeller.appendChild(navE_el);
    };
    if (t_el !== undefined) t_el.textContent = title; else return title;
  } catch (error) {
    console.error(error);
  }

};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

function CopyToLocalStorage(el, keyname) {
  // copies the the content from any element into the localstorage and
  // save it with that keyname
  localStorage.setItem(keyname, el.value.trim());
};


function RetrieveFromLocalStorage(key) {
  // Retrieves data with that key from the localstorage
  data = localStorage.getItem(key) !== null ? localStorage.getItem(key) : null // if key exists, return else return null
  return data;
};


async function upload_update_template({key, method, pk, topic_id } = {}) {
  /** A template for upload or update for topic or entry*/
  // if it's key is entry, then topic_id has to be passed
  key = key.trim().toLowerCase(); method = method.trim().toUpperCase();
  const msg = RetrieveFromLocalStorage(key);
  let data = '';

  if (key === 'topic') {
    if (method === 'POST') {data = {title: msg}}
     else if (method === 'PUT') {data = {id: pk, title: msg}}
      else throw new Error(`Unsupported method ${method}`);

  } else if (key === 'entry') {
    topic_id = topic_id !== undefined ? topic_id : await getApiObjectData({ endpoint: '/api/entry/', pk: pk, key: 'topic' })
    if (method === 'POST') {data = {topic: topic_id, text: msg}}
     else if (method === 'PUT') {data = {topic: topic_id, id: pk, text: msg}}
      else throw new Error(`Unsupported method ${method}`);

  } else throw new Error(`Invalid key: ${method}`);

  console.log(data);
  return JSON.stringify(data);
};


async function sendToServer({endpoint, pk, method, data} = {}) {
  method = method.toUpperCase().trim();
  const csrfToken = getCookie('csrftoken');
  let response = null;

  try {
    if (['POST', 'PUT'].includes(method)) {
      if (data !== undefined) {
        response = await fetch(endpoint + pk + '/', {
          method: method,
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: data,
        })
      } else throw new Error('Data cannot be undefined, if using HTTP method: ' + method);
  } else if (method === 'DELETE') {
      response = await fetch(endpoint + pk + '/', {
        method: method,
        headers: {
            'X-CSRFToken': csrfToken,
            // 'Authorization': 'Bearer your-token', // when implemented (if, themn put in DELETE)
          },
      })
  } else throw new Error('Unsupported HTTP Method: ' + method)

    if (!response.ok) throw new Error(`Failed: ${response.status}`); else {
      console.log(
      method === 'POST' ? 'Uploaded successfully' :
      method === 'PUT' ? 'Updated successfully' :
      method === 'DELETE' ? 'Deleted successfully' :
      'Done'
    );
    return true;
    
    };
  } catch (err) {
    console.error(err);
  }
};


async function SendReqToServer({ endpoint, pk, method, key, topic_id }){
  // Sends data to the server via the specified endpoint
  // topic_id is for entry objects
  // key is the key used to store in the localstorage, either 'topic' or 'entry'

  pk = pk !== undefined ? pk : get_pk_fromurlend();
  const data = await upload_update_template({ key: key, method: method, pk: pk, topic_id: topic_id });
  // ...sending process...
  let done = await sendToServer({ endpoint: endpoint, pk: pk, method: method, data: data });
  if (done) {localStorage.removeItem(key); console.log('deleted ' + key)};
};


async function RetrySendServer({endpoint, method, key, pk} = {}) {
  // Incase of system failure or net failure, check storage if data exists and forward to the server
  console.log('Checking for past data...')
  console.log(key);
  if (localStorage.getItem(key) !== null ? true : false) {
    console.log(`found ${key} item in storage.\nSending to server now...`)
    await SendReqToServer({ endpoint: endpoint, method: method, key: key, pk: pk})
  } else console.log('Nothing in storage, safe to proceed.');
};


