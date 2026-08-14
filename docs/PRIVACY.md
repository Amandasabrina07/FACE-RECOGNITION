# Privacy and Biometric Data Guidance

Face images and trained face-recognition models can contain sensitive biometric information. Treat them as private data unless every person involved has explicitly agreed to the intended use and publication.

## Do Not Commit

Do not commit these files to a public repository:

- `data/dataset/*.jpg`
- `data/dataset/*.png`
- `models/trainer.yml`
- `config/people.json` when it contains real names
- `firmware/esp32cam_capture/secrets.h`
- screenshots showing identifiable participants unless publication is authorized

The provided `.gitignore` blocks these paths by default.

## Recommended Practice

- Obtain permission before collecting face images.
- Explain why the data is collected and how long it will be retained.
- Store raw images and derived models in access-controlled storage.
- Delete datasets and models when they are no longer needed.
- Avoid using this educational prototype for access control, surveillance, employment decisions, or other high-impact decisions.
- Keep the ESP32-CAM on a trusted local network.
- Do not expose its HTTP capture endpoint directly to the public internet.

## Before Publishing

Run:

```bash
git status
```

Then confirm that no real face images, model files, names, IP-specific secrets, or credentials appear in the staged changes.
