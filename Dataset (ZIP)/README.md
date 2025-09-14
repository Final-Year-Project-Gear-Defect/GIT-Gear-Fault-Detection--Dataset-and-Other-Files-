> [!NOTE]
> In the actual Dataset, we observed that majority or almost all images available in the `test` split are free of defects

So, what we do is:
- we delete the `test` split
- instead, we split the actual `train` split into `train` and `test` split in ratio of `80:20`
- the `valid` split is kept intact 

Before custom filtering: `Old Dataset` | `gear-dataset`
- `Train:` 1092 images
- `Valid:` 305 images
- `Test:` 602 images
- `Total:` 1999 images

After custom filtering: `New Dataset` | `gear-defect-dataset`
- `Train:` 873 images
- `Valid:` 305 images
- `Test:` 219 images
- `Total:` 1397 images

The `Newest Dataset` | `gears-dataset` has
- removed `labels` subfolder inside the `test` split

The `Test Images` | `test-images` has
- manually selected 34 images for final testing purpose