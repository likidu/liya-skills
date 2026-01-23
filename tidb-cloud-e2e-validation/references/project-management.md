# Project Management Reference

## Feature Context

Projects in TiDB Cloud are organizational containers that group related clusters, manage team access, and control billing. Users interact with projects to organize their database resources.

## What to Validate

When evaluating Project Management UX, explore these areas:

- **Project CRUD operations** - Creating, viewing, editing, deleting projects
- **Member/role management** - Adding users, assigning roles, permission controls
- **Project settings** - Configuration options, naming, descriptions
- **Navigation** - How users find and switch between projects

## Key UX Questions

- Can a new user understand what a "Project" is and why they need one?
- Is it clear how projects relate to clusters?
- Are destructive actions (delete) appropriately guarded?
- Can power users manage multiple projects efficiently?

## Domain Terminology

| Term | Meaning |
|------|---------|
| Project | Organizational container for clusters and resources |
| Member | User with access to a project |
| Role | Permission level (Owner, Admin, Member, etc.) |
| Organization | Parent entity that contains multiple projects |
