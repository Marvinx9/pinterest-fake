# garantindo que esse código só será executado, se eu rodar esse arquivo
from fakepinterest import app

if __name__ == "__main__":
    app.run(debug=True)