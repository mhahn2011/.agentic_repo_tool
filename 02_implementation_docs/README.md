# Implementation Documentation

This folder contains technical guides and standards for developing and integrating tools into the `.agentic_repo_tools/` toolkit.

---

## Documents

### [Tool_Integration_Requirements.md](Tool_Integration_Requirements.md)
**Purpose:** Standards and checklist for making tools integration-ready

**Use this when:**
- Developing a new tool for the toolkit
- Preparing to integrate an existing tool
- Understanding toolkit integration patterns
- Setting up feature branch workflow

**Covers:**
- Feature branch development workflow
- Integration checklist (paths, outputs, documentation)
- Tool directory structure standards
- Registry.json entry requirements
- Testing with `04_test_repos/`
- Path conventions and relative navigation

---

## Quick Reference

**Developing a new tool?**
1. Read `Tool_Integration_Requirements.md` → understand standards
2. Create feature branch: `git checkout -b dev/<tool_name>`
3. Build at `.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/<tool_name>/`
4. Test using `03_test_repos/`
5. Follow integration checklist
6. Merge to main when stable

**Integration checklist summary:**
- ✅ No hardcoded paths (use relative navigation)
- ✅ Outputs to `02_project_specific_data/` (mirrored structure)
- ✅ Comprehensive README
- ✅ Dependencies documented
- ✅ Registry entry created
- ✅ `.gitignore` configured
- ✅ Tested in real projects

---

## Related Documentation

- **Architecture:** `.agentic_repo_tools/ARCHITECTURE.md` - Technical architecture of the toolkit
- **Development workflow:** `/claude.md` - Feature branch workflow, design principles
- **Planning:** `/01_planning_docs/` - Vision, roadmap, tool catalog
- **Testing:** `/03_test_repos/README.md` - Testing infrastructure

---

**Note:** This folder contains implementation guides, not planning docs. For strategic planning and vision, see `/01_planning_docs/`.
