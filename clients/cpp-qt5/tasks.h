

#ifndef PROGRESS_TASKS
#define PROGRESS_TASKS

#include <QtCore>
#include <QUrl>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QJsonDocument>
#include <QJsonObject>
#include <QDebug>

#define PROGRESS_URL_SUFFIX "/_ah/api/progressApi/v1/"

/**
    Base task for communicating with gae-process RESTful API
*/
class ProgressTask : public QObject
{
    Q_OBJECT
public:
    ProgressTask(QObject *parent = 0) : QObject(parent) {}
    
    void setApiKey(const QString &key) {
        _apikey = key;
    }
    
    void setNetworkAccessManager(QNetworkAccessManager *mgr) {
        _mgr = mgr;
    }
    
    void setAddress(QString addr) {
        _addr = addr;
    }
    
signals:
    void taskCompleted();
protected:
    
    QUrl urlFromAddressAndMethod(const QString &address, const QString &method) {
        return QUrl(address + PROGRESS_URL_SUFFIX + method);
    }
    
    QString _apikey;
    QString _addr;
    QNetworkAccessManager *_mgr;
};


/**
    List progresses.
*/
class ProgressListTask : public ProgressTask
{
    Q_OBJECT
public:
    ProgressListTask(QObject *parent = 0) : ProgressTask(parent) {}
    
    
    public slots:
    void run()
    {
        QUrl url = urlFromAddressAndMethod(_addr, "list");
        
        QUrlQuery query;
        query.addQueryItem("apikey", _apikey);
        url.setQuery(query);
        
        QNetworkRequest req(url);
        _reply = _mgr->get(req);

        QObject::connect(_reply, SIGNAL(finished()), this, SLOT(onReplyFinished()));
    }
    
    void onReplyFinished() {
        if ((_reply->error() == QNetworkReply::NoError)) {
            QJsonDocument doc = QJsonDocument::fromJson(_reply->readAll());
            if (!doc.isNull() && doc.isObject()) {
                QJsonObject root = doc.object();
                QJsonArray items = root["items"].toArray();
                qDebug() << "Received" << items.size() << "items";
                qDebug() << "----------";
                for (int i = 0; i < items.size(); ++i) {
                    QJsonObject item = items[i].toObject();
                    qDebug() << "id:" << item["id"].toString();
                    qDebug() << "created:" << item["created"].toString();
                    qDebug() << "title:" << item["title"].toString();
                    qDebug() << "progress:" << item["progress"].toInt();
                    qDebug() << "----------";
                }
            }
        } else {
            qDebug() << "Error:" << _reply->errorString();
        }
        
        _reply->deleteLater();
        emit taskCompleted();
    }
    
private:
    QNetworkReply *_reply;
};

/**
    Create progresses.
 */
class ProgressCreateTask : public ProgressTask
{
    Q_OBJECT
public:
    ProgressCreateTask(QObject *parent = 0) : ProgressTask(parent) {}
    
    void setTitle(const QString &title) {
        _title = title;
    }
    
    void setDescription(const QString &desc) {
        _desc = desc;
    }
    
    void setProgress(float p) {
        _progress = p;
    }
    
    public slots:
    void run()
    {
        QUrl url = urlFromAddressAndMethod(_addr, "create");
        
        QJsonObject j;
        j["apikey"] = _apikey;
        if (_title.size() > 0) j["title"] = _title;
        if (_desc.size() > 0) j["description"] = _desc;
        if (_title.size() > 0) j["progress"] = QString::number(_progress);
        
        QJsonDocument doc(j);
        QByteArray bytes = doc.toJson();
        QByteArray len = QByteArray::number(bytes.size());

        QNetworkRequest req(url);
        req.setRawHeader("Content-Type", "application/json");
        req.setRawHeader("Content-Length", len);
        
        _reply = _mgr->post(req, bytes);
        
        QObject::connect(_reply, SIGNAL(finished()), this, SLOT(onReplyFinished()));
    }
    
    void onReplyFinished() {
        if ((_reply->error() == QNetworkReply::NoError)) {
            QJsonDocument doc = QJsonDocument::fromJson(_reply->readAll());
            if (!doc.isNull() && doc.isObject()) {
                QJsonObject root = doc.object();
                qDebug() << "Created progress ID:" << root["id"].toString();
            }
        } else {
            qDebug() << "Error:" << _reply->errorString();
        }
        
        _reply->deleteLater();
        emit taskCompleted();
    }
    
private:
    QNetworkReply *_reply;
    QString _title, _desc;
    float _progress;
};


#endif
