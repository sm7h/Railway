<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="navbar">
        <button class="nav-button" id="main-btn" onclick="window.location.href='/main'">Main</button>
        <button class="nav-button" id="dashboard-btn" onclick="window.location.href='/dashboard'">Dashboard</button>
        <button class="nav-button" id="settings-btn" onclick="window.location.href='/settings'">Settings</button>
    </div>
    <div class="content">
        <h1>Welcome to your Dashboard</h1>
        <p>This is your main dashboard area.</p>
    </div>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function(){
            $(".nav-button").hover(function(){
                $(this).css("transform", "scale(1.1)");
            }, function(){
                $(this).css("transform", "scale(1)");
            });
        });
    </script>
</body>
</html>
