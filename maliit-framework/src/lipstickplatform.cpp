/* * This file is part of Maliit framework *
 *
 * Copyright (C) 2013 Jolla Ltd.
 * Copyright (C) 2019 Open Mobile Platform LLC.
 *
 * Contact: maliit-discuss@lists.maliit.org
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License version 2.1 as published by the Free Software Foundation
 * and appearing in the file LICENSE.LGPL included in the packaging
 * of this file.
 */

#include "lipstickplatform.h"

#include <QGuiApplication>
#include <QPlatformSurfaceEvent>
#include <qpa/qplatformnativeinterface.h>

#include <wayland-client.h>

namespace Maliit
{

static void setWaylandInputRegion(QPlatformNativeInterface *wliface, QWindow *window, const QRegion &region)
{
    if (wl_compositor *wlcompositor = static_cast<wl_compositor *>(
                wliface->nativeResourceForIntegration("compositor"))) {
        if (wl_surface *wlsurface = static_cast<wl_surface *>(
                    wliface->nativeResourceForWindow("surface", window))) {
            wl_region *wlregion = wl_compositor_create_region(wlcompositor);

            for (const QRect &rect : region.rects()) {
                wl_region_add(wlregion, rect.x(), rect.y(), rect.width(), rect.height());
            }

            wl_surface_set_input_region(wlsurface, wlregion);
            wl_surface_set_opaque_region(wlsurface, wlregion);
            wl_region_destroy(wlregion);

            wl_surface_commit(wlsurface);
        }
    }
}

class LipstickWindowPropertyBroadcaster : public QObject
{
public:
    LipstickWindowPropertyBroadcaster(QWindow *window)
        : QObject(window)
        , m_window(window)
    {
        m_window->installEventFilter(this);
    }

    bool eventFilter(QObject *object, QEvent *event)
    {
        if (object != m_window) {
            return false;
        } else switch (event->type()) {
        case QEvent::PlatformSurface: {
            QPlatformSurfaceEvent *platformEvent = static_cast<QPlatformSurfaceEvent *>(event);

            if (QPlatformWindow *handle = platformEvent->surfaceEventType() == QPlatformSurfaceEvent::SurfaceCreated
                    ? m_window->handle()
                    : nullptr) {
                QPlatformNativeInterface *native = QGuiApplication::platformNativeInterface();

                native->setWindowProperty(handle, QStringLiteral("CATEGORY"), QStringLiteral("overlay"));
                native->setWindowProperty(handle, QStringLiteral("MOUSE_REGION"), m_window->property("MOUSE_REGION"));

                setWaylandInputRegion(native, m_window, m_window->property("MOUSE_REGION").value<QRegion>());
            }
            return false;
        }
        case QEvent::DynamicPropertyChange: {
            QDynamicPropertyChangeEvent *propertyEvent = static_cast<QDynamicPropertyChangeEvent *>(event);
            if (QPlatformWindow *handle = propertyEvent->propertyName() == "MOUSE_REGION"
                    ? m_window->handle()
                    : nullptr) {
                QPlatformNativeInterface *native = QGuiApplication::platformNativeInterface();

                native->setWindowProperty(handle, QStringLiteral("MOUSE_REGION"), m_window->property("MOUSE_REGION"));
                setWaylandInputRegion(native, m_window, m_window->property("MOUSE_REGION").value<QRegion>());
            }
            return false;
        }
        default:
            return false;
        }
    }

private:
    QWindow * const m_window;
};

void LipstickPlatform::setupInputPanel(QWindow* window, Maliit::Position)
{
    new LipstickWindowPropertyBroadcaster(window);
}

void LipstickPlatform::setInputRegion(QWindow* window, const QRegion& region)
{
    window->setMask(region);
    window->setProperty("MOUSE_REGION", region);
}

} // namespace Maliit
