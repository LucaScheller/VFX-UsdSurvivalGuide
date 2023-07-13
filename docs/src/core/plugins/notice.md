# Notices/Event Listeners
Usd's event system is exposed via the [Notice](https://openusd.org/dev/api/group__group__tf___notification.html) class. It can be used to subscribe to different stage events or custom events to get notified about changes. 

A common case for using it with Python is sending update notifications to UIs.

## TL;DR - Notice/Event Listeners In-A-Nutshell
- The event system is uni-directional: The listeners subscribe to senders, but can't send information back to the senders. The senders are also not aware of the listeners, senders just send the event and the event system distributes it to the senders.
- The listeners are called synchronously in a random order (per thread where the listener was created), so make sure your listeners action is fast or forwards its execution into a separate thread. 

## Resources
- [Usd Notice API Docs](https://openusd.org/dev/api/class_usd_notice.html)
- [Tf Notification API Docs](https://openusd.org/dev/api/group__group__tf___notification.html)

## Notice code examples

#### Register/Revoke notice
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:noticeRegisterRevoke}}
```
~~~

#### Overview of built-in standard notices for stage change events
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:noticeCommon}}
```
~~~

#### Setup a custom notice:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:noticeCustom}}
```
~~~