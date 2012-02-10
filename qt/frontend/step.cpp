#include <QHBoxLayout>
#include <QGraphicsScene>
#include <QGraphicsEllipseItem>
#include <QGraphicsView>
#include <QGraphicsTextItem>
#include <QLabel>

#include "step.h"

Step::Step(QWidget *parent, QString text, QString index)
{
    setParent(parent);
    setFixedWidth(470);
    QHBoxLayout *layout = new QHBoxLayout(this);

    if (index != "") {
        QGraphicsScene *scene = new QGraphicsScene(0, 0, 20, 20);
        QGraphicsEllipseItem *item = new QGraphicsEllipseItem(0, 0, 20, 20);
        item->setBrush( Qt::yellow );
        item->setPos(0,0);
        scene->addItem(item);
        item->setPos(0,0);
        QGraphicsView *view = new QGraphicsView(scene);
        view->setFrameShape(QFrame::NoFrame);
        view->setBackgroundRole(QPalette::NoRole);
        view->setFixedSize(20, 20);
        QGraphicsTextItem *text = new QGraphicsTextItem(" "+ index, item);
        text->setTextWidth(20);
        layout->addWidget(view);
    } else {
        QWidget *widget = new QWidget(this);
        widget->setFixedWidth(50);
        layout->addWidget(widget);
    }

    QLabel *label = new QLabel(text);
    label->setWordWrap(true);
    label->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Maximum);
    layout->addWidget(label);
    show();

}

Step::~Step() {
    hide();
}