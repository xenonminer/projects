const worker = `
<!DOCTYPE HTML>
<html>
  <head>
    <title>Welcome to EaaS!</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
    <script>
        function adding() {
            var x = parseInt(document.getElementsByName("number")[0].value);
            var y = parseInt(document.getElementsByName("number")[1].value);
            var result = "Answer: " + (x + y);
            document.getElementById("test").innerHTML = result;
        }
    </script>
  </head>
  <body style="text-align: center;">
    <style>
      #fill {
        border-radius: 8px;
        padding: 10px;
        display: inline-block;
        cursor: text;
      }
    </style>
    <h1 style="padding-top: 5%;">Welcome to AaaS!</h1>
    <h2 style="padding-top: 2%;">Type the numbers that you want to add</h2>
    <form method="POST" action="/" style="padding-top: 2%;">
      <input type="text" name="number" id="fill" placeholder="first number" required> <br /><br />
      <input type="text" name="number" id="fill" placeholder="second number" required> <br /><br />
    </form>
    <button type="button" onclick="adding()">Add numbers</button>
    <p style="padding-top: 20px; color: red;"></p>

    <p id="test"></p>

  </body>
</html> `

//This grants access to index.js file when the user calls the worker function.
export default worker