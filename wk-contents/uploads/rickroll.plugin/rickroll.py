def setup(app):
    app.add_url_rule(
            "/rickroll",
            "_rickroll",
            lambda:'<meta http-equiv="refresh" content="0;url=https://www.youtube.com/watch?v=dQw4w9WgXcQ">'
            )
    print("Rickroll: /rickroll")
