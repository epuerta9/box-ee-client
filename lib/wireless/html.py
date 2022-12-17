

home_html = """
<!DOCTYPE html>
<title><Box-ee Device Page</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
<style>
input[type=text], select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input[type=submit] {
  width: 100%;
  background-color: #4CAF50;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

input[type=submit]:hover {
  background-color: #45a049;
}

div {
  border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px;
}
</style>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>URL Encoded Forms</title>
  </head>
  <body>
    <p>
        To generate a device api key go visit our documentation on how to generate one at https://docs.box-ee.com.
    </p>
    <form
      method="POST"
      enctype="application/json">
        <label for="ssid">SSID:</label><br>
      <input type="text" name="ssid" id="ssid" />
        <div></div>
        <label for="password">Password:</label><br>
      <input type="password" name="password" id=password" />
        <div></div>
        <label for="device-key">Device api Key:</label><br>
      <input type="text" name="device-key" id=device-key" />
        <div></div>
      <input type="submit" value="Submit" />
    </form>
  </body>
</html>
"""
#enctype="application/x-www-form-urlencoded">
#action="/urlencoded?apikey=device-key"
submitted_html = """
<!DOCTYPE html>
<title>Box-ee Device Page</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
<style>
input[type=text], select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input[type=submit] {
  width: 100%;
  background-color: #4CAF50;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

input[type=submit]:hover {
  background-color: #45a049;
}

div {
  border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px;
}
</style>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>URL Encoded Forms</title>
  </head>
  <body>
    <p>
        Saving your key and restarting the device! 
        if you want to update your api key at a later time, press the reset button for it to clear info and reboot.
    </p>    

  </body>
</html>
"""