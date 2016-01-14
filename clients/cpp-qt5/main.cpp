
#include <QtCore>
#include <QNetworkAccessManager>

#include "tasks.h"

int main(int argc, char* argv[])
{
    QCoreApplication app(argc, argv);
    QNetworkAccessManager mgr;
    
    ProgressListTask *task = new ProgressListTask(&app);
    task->setNetworkAccessManager(&mgr);
    task->setApiKey("d1535c766311cdf0dddf2269b6cd1120-91caff93-23fa-4692-a072-b8fbda064101");
    
    QObject::connect(task, SIGNAL(taskCompleted()), &app, SLOT(quit()));
    QTimer::singleShot(0, task, SLOT(run()));
    
    app.exec();
    
    return 0;
}