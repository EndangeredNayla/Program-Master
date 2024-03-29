# ============================================
# Program Master
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 2/29/2024
# License: MIT
# ============================================

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import queue
import threading
import customtkinter
import version
import webbrowser
import platform
import credits
from CTkToolTip import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Program Manager")
        self.geometry(f"{1330}x{780}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Program Master", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.browsersButton = customtkinter.CTkButton(self.sidebar_frame, text="App Installers", command=self.browsersView)
        self.browsersButton.grid(row=1, column=0, padx=20, pady=10)

        self.utilitiesButton = customtkinter.CTkButton(self.sidebar_frame, text="Utilities", command=self.UtilitiesView)
        self.utilitiesButton.grid(row=2, column=0, padx=20, pady=10)

        self.creditsButton = customtkinter.CTkButton(self.sidebar_frame, text="Credits", command=self.creditsView)
        self.creditsButton.grid(row=4, column=0, padx=20, pady=10)
        
        self.versionLabel = customtkinter.CTkLabel(self.sidebar_frame, text=f"Version: {version.appVersion}", anchor="w", font=("Arial", 14, "bold"))
        self.versionLabel.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.current_game_frame = None  # To keep track of the currently displayed game frame
    
        # set default values
        self.browsersButton.configure(state="disabled")
        self.current_game_frame = self.createAppInstaller()
        self.current_game_frame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), rowspan=3, sticky="nsew")


    def browsersView(self):
        self.browsersButton.configure(state="disabled")
        self.utilitiesButton.configure(state="enabled")
        self.creditsButton.configure(state="enabled")
        self.reset_game_frames()
        self.create_game_frame("App Installers")

    def UtilitiesView(self):
        self.browsersButton.configure(state="enabled")
        self.utilitiesButton.configure(state="disabled")
        self.creditsButton.configure(state="enabled")
        self.reset_game_frames()
        self.create_game_frame("Utilities")

    def creditsView(self):
        self.browsersButton.configure(state="enabled")
        self.utilitiesButton.configure(state="enabled")
        self.creditsButton.configure(state="disabled")
        self.reset_game_frames()
        self.create_game_frame("Credits")

    def reset_game_frames(self):
        # Reset the main frame to remove any existing game-specific widgets
        if self.current_game_frame:
            self.current_game_frame.destroy()

    def create_game_frame(self, game_name):
        # Create a new game frame based on the selected game_name
        self.reset_game_frames()

        if game_name == "App Installers":
            self.current_game_frame = self.createAppInstaller()
        elif game_name == "Utilities":
            self.current_game_frame = self.createUtilities()
        elif game_name == "Credits":
            self.current_game_frame = self.createCredits()
        self.current_game_frame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), rowspan=3, sticky="nsew")

    def createCredits(self):
        frame = customtkinter.CTkFrame(self, fg_color=("#fcfcfc", "#2e2e2e"))
        tabview = customtkinter.CTkTabview(frame, width=2000, height=650, fg_color=("#fcfcfc", "#323232"))
        tabview.pack(padx=20, pady=20)
        tabview.add("Credits")
        tabview.add("About")
        tabview.add("License")
        tabview.set("About")
        mit_license_widget = customtkinter.CTkLabel(tabview.tab("License"), width=80, height=20, text=(get_mit_license_text()))
        mit_license_widget.pack(padx=10, pady=10)
        credits_widget = customtkinter.CTkLabel(tabview.tab("Credits"), width=80, height=20, text=(get_credits_text()))
        credits_widget.pack(padx=10, pady=10)
        about_widget = customtkinter.CTkLabel(tabview.tab("About"), width=80, height=20, text=(get_about_text()))
        about_widget.pack(padx=10, pady=10)
        return frame

    def createAppInstaller(self):
        frame = customtkinter.CTkFrame(self, fg_color=("#fcfcfc", "#2e2e2e"))

        # Category Label
        self.label = customtkinter.CTkLabel(frame, text="Internet Browsers", font=("Arial", 18, "bold"))
        self.label.place(x=5, y=5)

        # Here for padding
        self.header_label = customtkinter.CTkLabel(frame, text="", font=("Arial", 18, "bold"))
        self.header_label.grid(row=0, column=1, sticky="w", padx=5, pady=(10, 0)) 

        # Create Arc
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openArc, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=1, column=0, sticky="w")
        self.arcToggle = customtkinter.CTkCheckBox(frame, text="Arc")
        self.arcToggle.grid(row=1, column=1, sticky="w")
        tooltipLabel = CTkToolTip(self.label, message="Experience a calmer, more personal internet in this browser designed for you.\nLet go of the clicks, the clutter, the distractions with the Arc browser.")
        if platform.system().lower() == "windows":
           self.arcToggle.configure(state=tk.DISABLED)
            
        # Create Brave
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openBrave, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=2, column=0, sticky="w")
        self.braveToggle = customtkinter.CTkCheckBox(frame, text="Brave")
        self.braveToggle.grid(row=2, column=1, sticky="w")

        # Create Chrome
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openChrome, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=3, column=0, sticky="w")
        self.chromeToggle = customtkinter.CTkCheckBox(frame, text="Chrome")
        self.chromeToggle.grid(row=3, column=1, sticky="w")

        # Create Chromium
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openChromium, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=4, column=0, sticky="w")
        self.chromiumToggle = customtkinter.CTkCheckBox(frame, text="Chromium")
        self.chromiumToggle.grid(row=4, column=1, sticky="w")

        # Create Edge
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openEdge, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=5, column=0, sticky="w")
        self.edgeToggle = customtkinter.CTkCheckBox(frame, text="Edge")
        self.edgeToggle.grid(row=5, column=1, sticky="w")

        # Create Firefox
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openFirefox, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=6, column=0, sticky="w")
        self.firefoxToggle = customtkinter.CTkCheckBox(frame, text="Firefox")
        self.firefoxToggle.grid(row=6, column=1, sticky="w")

        # Create Floorp
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openFloorp, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=7, column=0, sticky="w")
        self.floorpToggle = customtkinter.CTkCheckBox(frame, text="Floorp")
        self.floorpToggle.grid(row=7, column=1, sticky="w")

        # Create LibreWolf
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openLibreWolf, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=8, column=0, sticky="w")
        self.libreWolfToggle = customtkinter.CTkCheckBox(frame, text="LibreWolf")
        self.libreWolfToggle.grid(row=8, column=1, sticky="w")

        # Create Opera
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openOpera, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=9, column=0, sticky="w")
        self.operaToggle = customtkinter.CTkCheckBox(frame, text="Opera")
        self.operaToggle.grid(row=9, column=1, sticky="w")

        # Create Opera GX
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openOperaGX, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=10, column=0, sticky="w")
        self.operaGXToggle = customtkinter.CTkCheckBox(frame, text="Opera GX")
        self.operaGXToggle.grid(row=10, column=1, sticky="w")

        # Create Orion
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openOrion, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=11, column=0, sticky="w")
        self.orionToggle = customtkinter.CTkCheckBox(frame, text="Orion")
        self.orionToggle.grid(row=11, column=1, sticky="w")

        # Create Thorium
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openThorium, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=12, column=0, sticky="w")
        self.thoriumToggle = customtkinter.CTkCheckBox(frame, text="Thorium AVX2")
        self.thoriumToggle.grid(row=12, column=1, sticky="w")

        # Create Tor
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openTor, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=13, column=0, sticky="w")
        self.torToggle = customtkinter.CTkCheckBox(frame, text="Tor")
        self.torToggle.grid(row=13, column=1, sticky="w")

        # Create Ungoogled Chromium
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openUngoogled, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=14, column=0, sticky="w")
        self.ungoogledToggle = customtkinter.CTkCheckBox(frame, text="Ungoogled Chromium")
        self.ungoogledToggle.grid(row=14, column=1, sticky="w")

        # Create Vivaldi
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openVivaldi, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=15, column=0, sticky="w")
        self.vivaldiToggle = customtkinter.CTkCheckBox(frame, text="Vivaldi")
        self.vivaldiToggle.grid(row=15, column=1, sticky="w")

        # Here for padding
        self.header_label = customtkinter.CTkLabel(frame, text="", font=("Arial", 18, "bold"))
        self.header_label.grid(row=0, column=3, sticky="w", padx=5, pady=(10, 0)) 

        # Category Label
        self.label = customtkinter.CTkLabel(frame, text="Communications", font=("Arial", 18, "bold"))
        self.label.place(x=215, y=5)

        # Create Chatterino
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openChatterino, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=1, column=3, sticky="w")
        self.chatterinoToggle = customtkinter.CTkCheckBox(frame, text="Chatterino")
        self.chatterinoToggle.grid(row=1, column=4, sticky="w")

        # Create Discord
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openDiscord, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=2, column=3, sticky="w")
        self.discordToggle = customtkinter.CTkCheckBox(frame, text="Discord")
        self.discordToggle.grid(row=2, column=4, sticky="w")

        # Create Element
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openElement, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=3, column=3, sticky="w")
        self.elementToggle = customtkinter.CTkCheckBox(frame, text="Element")
        self.elementToggle.grid(row=3, column=4, sticky="w")

        # Create Ferdium
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openFerdium, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=4, column=3, sticky="w")
        self.ferdiumToggle = customtkinter.CTkCheckBox(frame, text="Ferdium")
        self.ferdiumToggle.grid(row=4, column=4, sticky="w")

        # Create Google Chat Desktop
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openGoogleChat, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=5, column=3, sticky="w")
        self.googleChatToggle = customtkinter.CTkCheckBox(frame, text="Google Chat Desktop")
        self.googleChatToggle.grid(row=5, column=4, sticky="w")
        if platform.system().lower() == "darwin":
           self.googleChatToggle.configure(state=tk.DISABLED)

        # Create Guilded
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openGuilded, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=6, column=3, sticky="w")
        self.guildedToggle = customtkinter.CTkCheckBox(frame, text="Guilded")
        self.guildedToggle.grid(row=6, column=4, sticky="w")

        # Create HexChat
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openHexChat, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=7, column=3, sticky="w")
        self.hexChatToggle = customtkinter.CTkCheckBox(frame, text="HexChat")
        self.hexChatToggle.grid(row=7, column=4, sticky="w")
        if platform.system().lower() == "darwin":
           self.hexChatToggle.configure(state=tk.DISABLED)

        # Create Jami
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openJami, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=8, column=3, sticky="w")
        self.jamiToggle = customtkinter.CTkCheckBox(frame, text="Jami")
        self.jamiToggle.grid(row=8, column=4, sticky="w")

        # Create Linphone
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openLinPhone, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=9, column=3, sticky="w")
        self.linphoneToggle = customtkinter.CTkCheckBox(frame, text="Linphone")
        self.linphoneToggle.grid(row=9, column=4, sticky="w")

        # Create Signal
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openSignal, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=10, column=3, sticky="w")
        self.signalToggle = customtkinter.CTkCheckBox(frame, text="Signal")
        self.signalToggle.grid(row=10, column=4, sticky="w")

        # Create Session
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openSession, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=11, column=3, sticky="w")
        self.sessionToggle = customtkinter.CTkCheckBox(frame, text="Session")
        self.sessionToggle.grid(row=11, column=4, sticky="w")

        # Create Skype
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openSkype, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=12, column=3, sticky="w")
        self.skypeToggle = customtkinter.CTkCheckBox(frame, text="Skype")
        self.skypeToggle.grid(row=12, column=4, sticky="w")

        # Create Slack
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openSlack, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=13, column=3, sticky="w")
        self.slackToggle = customtkinter.CTkCheckBox(frame, text="Slack")
        self.slackToggle.grid(row=13, column=4, sticky="w")

        # Create Teams
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openTeams, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=14, column=3, sticky="w")
        self.teamsToggle = customtkinter.CTkCheckBox(frame, text="Microsoft Teams")
        self.teamsToggle.grid(row=14, column=4, sticky="w")

        # Create Team Speak
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openTeamSpeak, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=15, column=3, sticky="w")
        self.teamSpeakToggle = customtkinter.CTkCheckBox(frame, text="TeamSpeak")
        self.teamSpeakToggle.grid(row=15, column=4, sticky="w")

        # Create Textual
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openTextual, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=16, column=3, sticky="w")
        self.textualToggle = customtkinter.CTkCheckBox(frame, text="Textual")
        self.textualToggle.grid(row=16, column=4, sticky="w")
        if platform.system().lower() == "windows":
           self.textualToggle.configure(state=tk.DISABLED)

        # Create Telegram
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openTeleGram, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=17, column=3, sticky="w")
        self.teleGramToggle = customtkinter.CTkCheckBox(frame, text="Telegram")
        self.teleGramToggle.grid(row=17, column=4, sticky="w")

        # Create Thunderbird
        self.label = customtkinter.CTkButton(frame, text="[?]", font=("Arial", 14, "bold"), text_color="aqua", command=self.openThunderbird, fg_color="#323232", hover_color="#323232", width=6)
        self.label.grid(row=18, column=3, sticky="w")
        self.thunderBirdToggle = customtkinter.CTkCheckBox(frame, text="Thunderbird")
        self.thunderBirdToggle.grid(row=18, column=4, sticky="w")

        # Text widget for displaying output
        self.output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=161, height=7, background="#323232", foreground="#ffffff")
        self.output_text.place(x=5, y=625)
    
        # Create and place the parseButton during the initialization
        self.parseButton = customtkinter.CTkButton(master=frame, command=self.parseDownloads, text="Download Programs")
        self.parseButton.place(x=1330 / 2 - 200, y=735)
        return frame

    def openArc(self):
        webbrowser.open('https://arc.net', new=2)

    def openBrave(self):
        webbrowser.open('https://brave.com', new=2)

    def openChrome(self):
        webbrowser.open('https://www.google.com/chrome', new=2)

    def openChromium(self):
        webbrowser.open('https://www.chromium.org/Home/', new=2)

    def openEdge(self):
        webbrowser.open('https://www.microsoft.com/en-us/edge', new=2)

    def openFirefox(self):
        webbrowser.open('https://www.mozilla.org/en-US/firefox/new', new=2)

    def openFloorp(self):
        webbrowser.open('https://floorp.app', new=2)

    def openLibreWolf(self):
        webbrowser.open('https://librewolf.net', new=2)

    def openOpera(self):
        webbrowser.open('https://www.opera.com', new=2)

    def openOperaGX(self):
        webbrowser.open('https://www.opera.com/gx', new=2)

    def openOrion(self):
        webbrowser.open('https://kagi.com/orion', new=2)

    def openThorium(self):
        webbrowser.open('https://thorium.rocks', new=2)

    def openTor(self):
        webbrowser.open('https://www.torproject.org/download', new=2)

    def openUngoogled(self):
        webbrowser.open('https://ungoogled-software.github.io/ungoogled-chromium-binaries', new=2)

    def openVivaldi(self):
        webbrowser.open('https://vivaldi.com', new=2)

    def openChatterino(self):
        webbrowser.open('https://chatterino.com', new=2)

    def openDiscord(self):
        webbrowser.open('https://www.discord.com', new=2)

    def openFerdium(self):
        webbrowser.open('https://ferdium.org', new=2)

    def openGuilded(self):
        webbrowser.open('https://www.guilded.gg', new=2)

    def openTextual(self):
        webbrowser.open('https://www.codeux.com/textual', new=2)

    def openTeamSpeak(self):
        webbrowser.open('https://www.teamspeak.com/en', new=2)

    def openGoogleChat(self):
        webbrowser.open('https://github.com/squalou/google-chat-linux')

    def openHexChat(self):
        webbrowser.open('https://hexchat.github.io')

    def openJami(self):
        webbrowser.open('https://jami.net')

    def openElement(self):
        webbrowser.open('https://element.io')

    def openLinPhone(self):
        webbrowser.open('https://www.linphone.org')

    def openSession(self):
        webbrowser.open('https://getsession.org')

    def openSignal(self):
        webbrowser.open('https://signal.org')

    def openSkype(self):
        webbrowser.open('https://www.skype.com')

    def openSlack(self):
        webbrowser.open('https://slack.com')

    def openTeams(self):
        webbrowser.open('https://www.microsoft.com/en/microsoft-teams/group-chat-software')

    def openTeleGram(self):
        webbrowser.open('https://telegram.org')

    def openThunderbird(self):
        webbrowser.open('https://www.thunderbird.net')


    def parseDownloads(self):
        # Disable the button before executing commands
        self.parseButton.configure(state=tk.DISABLED)
        
        if platform.system().lower() == "windows":
            commands = "winget install --accept-package-agreements --accept-source-agreements "
        else:
            commands = "brew install --display-times "
        
        if platform.system().lower() == "darwin":
            if self.arcToggle.get() == 1:
                commands = commands + "arc "
            else:
                pass

        if self.braveToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Brave.Brave "
            else:
                commands = commands + "brave-browser "
    
        if self.chromeToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Google.Chrome "
            else:
                commands = commands + "google-chrome "

        if self.chromiumToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Hibbiki.Chromium "
            else:
                commands = commands + "chromium " 

        if self.edgeToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Microsoft.Edge "
            else:
                commands = commands + "microsoft-edge "

        if self.firefoxToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Mozilla.Firefox "
            else:
                commands = commands + "firefox "

        if self.floorpToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Ablaze.Floorp "
            else:
                commands = commands + "floorp "

        if self.libreWolfToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "LibreWolf.LibreWolf "
            else:
                commands = commands + "librewolf "

        if self.operaToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Opera.Opera "
            else:
                commands = commands + "opera "

        if self.operaGXToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Opera.OperaGX "
            else:
                commands = commands + "opera-gx "

        if self.orionToggle.get() == 1:
            if platform.system().lower() == "windows":
                pass
            else:
                commands = commands + "orion "

        if self.thoriumToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Alex313031.Thorium.AVX2 "
            else:
                commands = commands + "alex313031-thorium "

        if self.torToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "TorProject.TorBrowser "
            else:
                commands = commands + "tor-browser "

        if self.ungoogledToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "eloston.ungoogled-chromium "
            else:
                commands = commands + "eloston-chromium "

        if self.vivaldiToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "VivaldiTechnologies.Vivaldi "
            else:
                commands = commands + "vivaldi "

        if self.discordToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Discord.Discord "
            else:
                commands = commands + "discord "

        if self.ferdiumToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Ferdium.Ferdium "
            else:
                commands = commands + "ferdium "

        if self.guildedToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Guilded.Guilded "
            else:
                commands = commands + "guilded "

        if self.teamSpeakToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "TeamSpeakSystems.TeamSpeakClient "
            else:
                commands = commands + "teamspeak-client "

        if self.textualToggle.get() == 1:
            if platform.system().lower() == "windows":
                pass
            else:
                commands = commands + "textual "

        if self.googleChatToggle.get() == 1:
            if platform.system().lower() == "darwin":
                pass
            else:
                commands = commands + "squalou.google-chat-linux "

        if self.chatterinoToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "ChatterinoTeam.Chatterino "
            else:
                commands = commands + "chatterino "

        if self.hexChatToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "HexChat.HexChat "
            else:
                pass

        if self.jamiToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "SFLinux.Jami "
            else:
                commands = commands + "jami "

        if self.linPhoneToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "BelledonneCommunications.Linphone "
            else:
                commands = commands + "linphone "

        if self.elementToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Element.Element "
            else:
                commands = commands + "element "

        if self.sessionToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Oxen.Session "
            else:
                commands = commands + "session "

        if self.signalToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "OpenWhisperSystems.Signal "
            else:
                commands = commands + "signal "

        if self.skypeToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Microsoft.Skype "
            else:
                commands = commands + "skype "

        if self.slackToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "SlackTechnologies.Slack "
            else:
                commands = commands + "slack "

        if self.teamsToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Microsoft.Teams "
            else:
                commands = commands + "microsoft-teams "


        if self.telegramToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Telegram.TelegramDesktop "
            else:
                commands = commands + "telegram "

        if self.thunderbirdToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Mozilla.Thunderbird "
            else:
                commands = commands + "thunderbird "

        def execute_command():
            if commands:
                process = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

                # Function to read the output asynchronously
                def read_output(file, queue, lock):
                    while True:
                        line = file.readline()
                        if not line:
                            break
                        with lock:
                            queue.put(line)

                # Set up queues and lock
                stdout_queue = queue.Queue()
                stderr_queue = queue.Queue()
                output_lock = threading.Lock()

                # Create file event handlers
                stdout_handler = threading.Thread(target=read_output, args=(process.stdout, stdout_queue, output_lock))
                stderr_handler = threading.Thread(target=read_output, args=(process.stderr, stderr_queue, output_lock))

                # Start file event handlers
                stdout_handler.start()
                stderr_handler.start()

                def check_output():
                    with output_lock:
                        while not stdout_queue.empty():
                            self.output_text.configure(state='normal')
                            self.output_text.insert(tk.END, stdout_queue.get())
                            self.output_text.yview(tk.END)  # Scroll to the bottom
                            self.output_text.configure(state='disabled')

                        while not stderr_queue.empty():
                            self.output_text.configure(state='normal')
                            self.output_text.insert(tk.END, stderr_queue.get())
                            self.output_text.yview(tk.END)  # Scroll to the bottom
                            self.output_text.configure(state='disabled')

                    if process.poll() is None:
                        # The process is still running, so check again after a short delay
                        self.output_text.after(100, check_output)
                    else:
                        # Command finished, clean up
                        stdout_handler.join()
                        stderr_handler.join()

                        # Enable the button after command execution is complete
                        self.parseButton.configure(state=tk.NORMAL)

                # Start checking for output
                check_output()

        # Start executing commands
        execute_command()

if __name__ == "__main__":
    app = App()
    app.mainloop()
