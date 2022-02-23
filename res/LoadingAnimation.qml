import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: root
    clip: true

    property bool run: false

    property color indicator_color: 'grey'

    Rectangle {
        id: anim_rect
        anchors.fill: parent
        clip: true
        color: root.color
        radius: height / 2

        Rectangle {
            id: indicator
            anchors.fill: parent
            anchors.margins: 15
            color: root.indicator_color
            radius: height / 2

            Rectangle {
                anchors.fill: parent
                anchors.margins: 5
                color: root.color
                radius: height / 2
            }
        }

        Rectangle {
            color: root.color
            height: parent.height
            width: parent.width/2
            anchors.top: parent.top
            anchors.right: parent.horizontalCenter
        }

        Rectangle {
            color: root.color
            height: parent.height/2
            width: parent.width
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    PropertyAnimation {
        target: anim_rect
        running: root.run
        property: 'rotation'
        duration: 750
        from: 0
        to: 360
        loops: Animation.Infinite
        easing: Easing.OutCubic

        onFinished: { indicator_hide.start(); }
    }

    PropertyAnimation {
        id: indicator_hide
        target: indicator
        property: 'opacity'
        duration: 150
        from: 1
        to: 0

        onFinished: { anim_rect.visible = false; }
    }
}
