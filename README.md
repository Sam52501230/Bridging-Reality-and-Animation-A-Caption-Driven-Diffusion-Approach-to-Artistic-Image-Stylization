# Bridging Reality and Animation: A Caption-Driven Diffusion Approach to Artistic Image Stylization

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Conference: ICCIS 2025](https://img.shields.io/badge/Conference-ICCIS%202025-green.svg)](https://scrs.in/conference/iccis2025)

**Accepted at: 7th International Conference on Communication and Intelligent Systems (ICCIS 2025)**  
**Published in: Springer Lecture Notes in Networks and Systems (Scopus-indexed)**  
**Paper ID: 280 | Presented: September 26-27, 2025**

Official implementation of the paper "Bridging Reality and Animation: A Caption-Driven Diffusion Approach to Artistic Image Stylization" accepted at ICCIS 2025 and published in Springer LNNS.

## 🎯 Overview

This project presents a modular, caption-based image artistic transformation framework that converts real photographs into anime-inspired illustrations, drawing inspiration from Studio Ghibli and Soft Serve visual styles. The system achieves high creative stylization while maintaining strong semantic alignment between original images and resulting artwork.


## 🏆 Conference Details

- **Conference**: 7th International Conference on Communication and Intelligent Systems (ICCIS 2025)
- **Dates**: September 26-27, 2025
- **Venue**: BITS Pilani, K K Birla Goa Campus, India (Hybrid Mode)
- **Proceedings**: Springer Lecture Notes in Networks and Systems (Scopus-indexed)
- **Paper ID**: 280
- **Presentation Date**: September 26-27, 2025
- **Status**: ✅ Accepted and Presented

## ✨ Key Features

- **Two-Stage Pipeline**: Image captioning followed by caption-guided diffusion
- **Multiple Styles**: Support for Ghibli and SoftServe artistic styles
- **Semantic Preservation**: Strong content alignment through caption guidance
- **State-of-the-Art Performance**: FID 26.4, CLIP Similarity 0.73 (Ghibli style)

## 🏗️ Architecture

### Stage 1: Image Captioning
- **Encoder**: ResNet-based CNN for feature extraction
- **Decoder**: Transformer for autoregressive caption generation
- **Training**: MS-COCO dataset with cross-entropy loss

### Stage 2: Diffusion-Based Stylization
- **Model**: U-Net based denoising diffusion model
- **Conditioning**: Text embeddings from generated captions
- **Sampling**: PNDM scheduler with 50 steps

## 📊 Results

| Method | FID ↓ | CLIP Similarity ↑ |
|--------|-------|------------------|
| CycleGAN | 41.2 | 0.61 |
| StyleGAN2 | 38.7 | 0.65 |
| Stable Diffusion v1.5 | 30.5 | 0.68 |
| **Ours (Ghibli)** | **26.4** | **0.73** |
| **Ours (SoftServe)** | **28.1** | **0.70** |

