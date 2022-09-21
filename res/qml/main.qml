import QtQuick 2.15
import QtQuick.Window 2.12
import QtQuick.Controls 2.12

Window {
    id: root

    // Colors

    property color color_base: "#EEFFFF"
    property color color_accent: "#f0f4f2"
    property color color_hover: "#F6F6F6"
    property color color_press: "#E8E8E8"
    property color color_select: 'white'

    // Window Settings

    title: "WebParser"
    visible: true
    color: color_base
    width: 900
    height: 600
    minimumHeight: 600
    minimumWidth: 900
    maximumHeight: 600
    maximumWidth: 900

    //  Title

    Header {
        anchors.fill: parent
    }

    // Settings Button

    Button {
        id: settings

        height: 60
        width: height

        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 25
        anchors.topMargin: 25

        background: Rectangle { radius: height / 2;
            color: settings.pressed ? color_press : settings.hovered ? 'white' : 'transparent'; }

        icon.source: "../icons/gear.png"
        icon.color: 'transparent'
        icon.width: width * 0.9
        icon.height: width * 0.9

        onReleased: { settings_popup.open(); }
    }

    // Settings Popup Main

    SettingsPopup {
        id: settings_popup
        height: parent.height * 0.98
        width: parent.width * 0.98
        anchors.centerIn: parent
    }

    // Additional Settings

    AddSettings {
        id: add_settings
        width: 200
        height: 300
        radius: 30
        x: 45
        y: 150
    }

    // Settings Url

    UrlSettings {
        id: url_settings
        width: 575
        height: 300
        x: 280
        y: 150
    }

    // Button PARSE

    Button {
        id: startParse

        enabled: url_settings.url != ''

        width: 150
        height: 50

        text: "Parse"
        font.pixelSize: height / 2

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 50

        background: Rectangle { radius: 5; border.width: 1;
            color: startParse.pressed ? color_press : startParse.hovered ? color_hover : 'white'; }

        onReleased: {
            parser.parse(url_settings.url, add_settings.timeout, url_settings.folder,
                add_settings.archive, add_settings.merge, url_settings.count_of_chapters);
            download_popup.open();
        }
    }

    // Download popup

    DownloadPopup {
        id: download_popup
        width: parent.width * 0.95
        height: parent.height * 0.95
        anchors.centerIn: parent
    }
}
