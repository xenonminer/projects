import worker from './worker'
// This imports the worker file, goes ahead to take the HTML you created earlier,
// and make it your new response.
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
//the addEventListener function listens for a fetch request from the worker
//the event.respondWith() method allows you to provide a response to the fetch.
})

async function handleRequest(request) {
  return new Response(worker, {
    headers: { 'content-type': 'text/html' },
		// The async function recieves the new request and 
		// returns new custom response of text/html type.
  })
}