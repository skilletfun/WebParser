import QtQuick 2.15
import QtQuick.Controls 2.14

Rectangle {
    property bool merge: do_merge.checked
    property bool archive: do_archive.checked
    property int timeout: slider_timeout.value

    width: 200
    height: 300
    radius: 30
    border.color: "black"

    // Title

    Text {
        text: 'Add. settings'
        font.family: 'Arial'
        font.pixelSize: 18
        font.italic: true
        anchors.horizontalCenter: parent.horizontalCenter
        y: 20
    }

    Column {
        anchors.fill: parent
        anchors.margins: 20
        anchors.topMargin: 50
        spacing: 5

        // Archive

        Row {
            height: 35
            width: parent.width
            Text {
                text: 'Archive\t'
                font.pixelSize: 17
                font.family: 'Arial'
                anchors.verticalCenter: do_archive.verticalCenter
            }

            Switch { id: do_archive; }
        }

        // Merge into one image

        Row {
            height: 35
            width: parent.width
            Text {
                text: 'Merge\t'
                font.pixelSize: 17
                font.family: 'Arial'
                anchors.verticalCenter: do_merge.verticalCenter
            }

            Switch { id: do_merge; }
        }
        Rectangle { color: 'transparent'; width: 1; height: 1; }

        // Timeout

        Text {
            text: 'Timeout: ' + String(slider_timeout.value)
            font.family: 'Arial'
            font.pixelSize: 17
        }

        // Timeout Slider

        Slider {
            id: slider_timeout
            from: 0
            to: 15
            value: 0
            stepSize: 1
            anchors.left: parent.left
            anchors.right: parent.right
        }
    }
}


