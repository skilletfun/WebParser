import QtQuick 2.15
import QtQuick.Controls 2.14

Rectangle {
    property bool merge: do_merge.checked
    property bool archive: do_archive.checked

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

        // Waifu2x

        Row {
            height: 35
            width: parent.width
            Text {
                text: 'Waifu2x\t'
                font.pixelSize: 17
                font.family: 'Arial'
                anchors.verticalCenter: do_waifu.verticalCenter
            }

            Switch { id: do_waifu; }
        }

        // Upload to GDrive

        Row {
            height: 35
            width: parent.width
            Text {
                text: 'GDrive\t'
                font.pixelSize: 17
                font.family: 'Arial'
                anchors.verticalCenter: upload.verticalCenter
            }

            Switch { id: upload; }
        }
    }
}


