---
title: Welcome
sidebarDepth: 0
---

<div align="center" style="margin-top:50px; margin-bottom:40px;">
    <img src="/illustrations/cloud-illustration.svg"  width=300 >
</div>

# Orchestration

When you want to run and monitor many flows, maintaining their state and inspecting their progress can be difficult without some extra tooling.

Prefect Core's server and Prefect Cloud are two ready-to-use state database and UI backends that automatically extend the Prefect Core engine with a rich GraphQL API to make orchestration of your flows easy.

Prefect Core's server is an open source, lightweight version of our highly-available, production-ready product Prefect Cloud.

Depending on your needs, you might want to try the open source server in Prefect Core, [sign up for our free Prefect Cloud "Developer" tier](https://cloud.prefect.io/), or [scale up to a bigger Prefect Cloud license](https://www.prefect.io/pricing/). All of your Prefect flows will work seamlessly on any of these backends, so you won't need to change any of your flow code to change between them.


##### Prefect Core server

Prefect Core ships with an open-source backend and UI that automatically extends the Prefect Core engine with:

- a full GraphQL API
- a complete UI for flows and jobs
- automatic and asynchronous scheduling and alerting

Get started by running `prefect server start` and navigate to `http://localhost:8080`.

**Note:** Prefect Server requires both Docker and Docker Compose.

##### Prefect Cloud

Prefect Cloud is a fully hosted, production-ready backend for Prefect Core. If you've used Prefect Core's server, Prefect Cloud is a drop in replacement that provides some enhanced features, including:

- permissions and authorization
- performance enhancements that allow you to scale
- agent monitoring
- secure runtime secrets and parameters
- team management
- SLAs
- many more features...

As you read through these docs, when you see the <Badge text="Cloud"/> badge, you'll know if a feature is supported only in Prefect Cloud or not.

We know one of these solutions will minimize your [negative engineering](https://medium.com/the-prefect-blog/positive-and-negative-data-engineering-a02cb497583d) burden, and get you back to the code you really want to write.

Happy engineering!

_- The Prefect Team_
