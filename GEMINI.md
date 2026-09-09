# Blacksmith Knight — Agent Execution Rules

## 1. Autonomous Milestone Execution
- **Zero-Interruption Policy**: Do NOT pause or ask for confirmation on intermediate steps, file creations, file edits, command runs, test suites, or frontend builds. Execute all tasks within the requested milestone autonomously from start to finish.
- **Delete Confirmation Boundary**: Ask permission ONLY before deleting files or major components, and ONLY at the conclusion of the milestone.

## 2. Milestone Git & Verification Protocol
For each milestone:
1. **Branch**: Create and checkout `feature/MilestoneXX` (e.g. `feature/Milestone15`) from `develop`.
2. **Implementation**: Implement models, services, endpoints, and frontend components as defined in the master development program.
3. **Quality Gate**:
   - Backend tests must pass: `.\backend\.venv\Scripts\pytest tests\backend -v`
   - Frontend production build must succeed: `npm --prefix frontend run build`
4. **Documentation**:
   - Update `docs/Blacksmith_Knight_Forging_Heaven_Development_Program_and_Work_Log.md` marking milestone tasks as COMPLETE with implementation details and test notes.
   - Update `docs/walkthrough.md`.
5. **Merge & Push**:
   - Commit and push `feature/MilestoneXX` to `origin/feature/MilestoneXX`.
   - Checkout `develop`, merge `feature/MilestoneXX`, and push `develop` to `origin/develop`.
6. **Stop**: Stop execution upon milestone completion and report results.

## 3. Communication Style
- Caveman mode: direct, terse, minimal fluff, code-strong.
- Every file reference must be a clickable markdown link using `file:///` scheme (e.g., `[filename](file:///path/to/file)`).
