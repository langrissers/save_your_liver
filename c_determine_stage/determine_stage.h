#pragma once
#ifndef _DETERMINE_STAGE_H_
#define _DETERMINE_STAGE_H_
#ifdef DLLDEMO1_EXPORTS
#define EXPORTS_DEMO _declspec( dllexport )
#else
#define EXPORTS_DEMO _declspec(dllimport)
#endif
extern "C" EXPORTS_DEMO int determine_stage();
#endif
