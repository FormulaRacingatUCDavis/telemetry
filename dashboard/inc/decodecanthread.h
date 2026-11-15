#pragma once

#include <QObject>
#include <QDebug>
#include <QThread>

#include "daq.h" 

namespace dashboard
{
    class DecodeCanThread : public QObject
    {
        Q_OBJECT

    public:
        // Store the initialized manager pointer
        dashboard::CANManager* canManager = nullptr; 

    public slots:
        
        void startContinuousDecoding()
        {
            QThread *currThread = QThread::currentThread();

            // checks if interruption signal is requested by thread it is on
            while (!currThread->isInterruptionRequested())
            {
                canManager->decode_can(dashboard::Variables::instance());   
                QThread::msleep(1);
            }
        }
        
        // Custom slot to receive the manager from the main thread
        void setCANManager(dashboard::CANManager* manager)
        {
            canManager = manager;
        }
    };
}