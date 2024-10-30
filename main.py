from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
import sys
import subprocess
import threading
import time

button_text = "Update the Software"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Git Pull with Authentication')
        self.setGeometry(100, 100, 280, 80)

        layout = QVBoxLayout()

        self.updateButton = QPushButton(button_text, self)
        layout.addWidget(self.updateButton)

        self.updateButton.clicked.connect(self.on_updateButton_clicked)

        self.loadingScreen = LoadingScreen()

        self.setLayout(layout)

    def on_updateButton_clicked(self):
        self.loadingScreen.startAnimation()
        self.loadingScreen.show()

        # Run the Git update in a separate thread to avoid blocking the UI
        threading.Thread(target=self.run_git_update).start()

    def run_git_update(self):
        username = "BurhanKeskin"
        repo_name = "Duyuru-Sorgulama"
        token = read_token_file()
        local_repo_path = "/home/burhankeskin/Documents/Duyuru-Sorgulama"

        # Create the necessary URL by using username and token for GitHub
        remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"

        try:
            print("The repository's remote URL is being updated....")
            
            # Update the remote URL
            subprocess.run(["git", "-C", local_repo_path, "remote", "set-url", "origin", remote_url], check=True)

            # Execute "reset" and "clean" commands to be able to synchronize the local repo with the remote repo completely.
            print("Local repo is being reset...")
            subprocess.run(["git", "-C", local_repo_path, "reset", "--hard"], check=True)
            subprocess.run(["git", "-C", local_repo_path, "clean", "-fd"], check=True)

            # Last changes are being pulled from GitHub...
            print("Last changes are being pulled from GitHub...")
            result = subprocess.run(["git", "-C", local_repo_path, "pull", "origin", "master"], check=True, capture_output=True, text=True)

            print("Git pull successful.")
            print(result.stdout)

            # Stop the loading animation after the process is complete
            self.loadingScreen.stopAnimation()
            
        except subprocess.CalledProcessError as e:
            print(f"An error has occurred.\nError: {e.stderr}")

        # Wait for 5 seconds before rebooting
        time.sleep(5)
        print("System will reboot now...")
        subprocess.run(["reboot"], check=True)
        


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(150, 150)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self.label_animation = QLabel(self)

        self.movie = QMovie("/home/burhankeskin/Downloads/loading.gif")
        self.label_animation.setMovie(self.movie)

        layout = QVBoxLayout()
        layout.addWidget(self.label_animation)
        self.setLayout(layout)

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()
        self.close()


def read_token_file():
    path = "/home/burhankeskin/Documents/token.txt"

    try:
        with open(path, 'r') as file:
            text_content = file.read().strip()
            print("Token file's content was successfully read.")
            return text_content
    except FileNotFoundError:
        print(f"{path} couldn't be found.")
    except IOError as e:
        print(f"File Reading Error: {e}")


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


main()
