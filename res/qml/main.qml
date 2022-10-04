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
            parser.parse(url_settings.url, url_settings.count_of_chapters);
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
