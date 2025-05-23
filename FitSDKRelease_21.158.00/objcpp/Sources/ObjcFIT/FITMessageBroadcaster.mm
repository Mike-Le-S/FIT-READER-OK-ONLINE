/////////////////////////////////////////////////////////////////////////////////////////////
// Copyright 2024 Garmin International, Inc.
// Licensed under the Flexible and Interoperable Data Transfer (FIT) Protocol License; you
// may not use this file except in compliance with the Flexible and Interoperable Data
// Transfer (FIT) Protocol License.
/////////////////////////////////////////////////////////////////////////////////////////////
// ****WARNING****  This file is auto-generated!  Do NOT edit this file.
// Profile Version = 21.158.0Release
// Tag = production/release/21.158.0-0-gc9428aa
/////////////////////////////////////////////////////////////////////////////////////////////

#import "FITMessageBroadcaster.h"
#import "FITTypes.h"

@implementation FITMessageBroadcaster

- (instancetype)init {
    self = [super init];
    if (self) {

    }
    return self;
}

- (void)onMesg:(FITMessage*)message {
    [self.mesgDelegate onMesg:message];

    switch ([message getNum]) {
        case FITMesgNumFileId:
            [self.fitFileIdMesgDelegate onFileIdMesg:[[FITFileIdMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumFileCreator:
            [self.fitFileCreatorMesgDelegate onFileCreatorMesg:[[FITFileCreatorMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumTimestampCorrelation:
            [self.fitTimestampCorrelationMesgDelegate onTimestampCorrelationMesg:[[FITTimestampCorrelationMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSoftware:
            [self.fitSoftwareMesgDelegate onSoftwareMesg:[[FITSoftwareMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSlaveDevice:
            [self.fitSlaveDeviceMesgDelegate onSlaveDeviceMesg:[[FITSlaveDeviceMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumCapabilities:
            [self.fitCapabilitiesMesgDelegate onCapabilitiesMesg:[[FITCapabilitiesMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumFileCapabilities:
            [self.fitFileCapabilitiesMesgDelegate onFileCapabilitiesMesg:[[FITFileCapabilitiesMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumMesgCapabilities:
            [self.fitMesgCapabilitiesMesgDelegate onMesgCapabilitiesMesg:[[FITMesgCapabilitiesMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumFieldCapabilities:
            [self.fitFieldCapabilitiesMesgDelegate onFieldCapabilitiesMesg:[[FITFieldCapabilitiesMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumDeviceSettings:
            [self.fitDeviceSettingsMesgDelegate onDeviceSettingsMesg:[[FITDeviceSettingsMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumUserProfile:
            [self.fitUserProfileMesgDelegate onUserProfileMesg:[[FITUserProfileMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHrmProfile:
            [self.fitHrmProfileMesgDelegate onHrmProfileMesg:[[FITHrmProfileMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSdmProfile:
            [self.fitSdmProfileMesgDelegate onSdmProfileMesg:[[FITSdmProfileMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumBikeProfile:
            [self.fitBikeProfileMesgDelegate onBikeProfileMesg:[[FITBikeProfileMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumConnectivity:
            [self.fitConnectivityMesgDelegate onConnectivityMesg:[[FITConnectivityMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumWatchfaceSettings:
            [self.fitWatchfaceSettingsMesgDelegate onWatchfaceSettingsMesg:[[FITWatchfaceSettingsMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumOhrSettings:
            [self.fitOhrSettingsMesgDelegate onOhrSettingsMesg:[[FITOhrSettingsMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumTimeInZone:
            [self.fitTimeInZoneMesgDelegate onTimeInZoneMesg:[[FITTimeInZoneMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumZonesTarget:
            [self.fitZonesTargetMesgDelegate onZonesTargetMesg:[[FITZonesTargetMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSport:
            [self.fitSportMesgDelegate onSportMesg:[[FITSportMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHrZone:
            [self.fitHrZoneMesgDelegate onHrZoneMesg:[[FITHrZoneMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSpeedZone:
            [self.fitSpeedZoneMesgDelegate onSpeedZoneMesg:[[FITSpeedZoneMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumCadenceZone:
            [self.fitCadenceZoneMesgDelegate onCadenceZoneMesg:[[FITCadenceZoneMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumPowerZone:
            [self.fitPowerZoneMesgDelegate onPowerZoneMesg:[[FITPowerZoneMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumMetZone:
            [self.fitMetZoneMesgDelegate onMetZoneMesg:[[FITMetZoneMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumDiveSettings:
            [self.fitDiveSettingsMesgDelegate onDiveSettingsMesg:[[FITDiveSettingsMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumDiveAlarm:
            [self.fitDiveAlarmMesgDelegate onDiveAlarmMesg:[[FITDiveAlarmMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumDiveApneaAlarm:
            [self.fitDiveApneaAlarmMesgDelegate onDiveApneaAlarmMesg:[[FITDiveApneaAlarmMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumDiveGas:
            [self.fitDiveGasMesgDelegate onDiveGasMesg:[[FITDiveGasMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumGoal:
            [self.fitGoalMesgDelegate onGoalMesg:[[FITGoalMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumActivity:
            [self.fitActivityMesgDelegate onActivityMesg:[[FITActivityMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSession:
            [self.fitSessionMesgDelegate onSessionMesg:[[FITSessionMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumLap:
            [self.fitLapMesgDelegate onLapMesg:[[FITLapMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumLength:
            [self.fitLengthMesgDelegate onLengthMesg:[[FITLengthMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumRecord:
            [self.fitRecordMesgDelegate onRecordMesg:[[FITRecordMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumEvent:
            [self.fitEventMesgDelegate onEventMesg:[[FITEventMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumDeviceInfo:
            [self.fitDeviceInfoMesgDelegate onDeviceInfoMesg:[[FITDeviceInfoMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumDeviceAuxBatteryInfo:
            [self.fitDeviceAuxBatteryInfoMesgDelegate onDeviceAuxBatteryInfoMesg:[[FITDeviceAuxBatteryInfoMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumTrainingFile:
            [self.fitTrainingFileMesgDelegate onTrainingFileMesg:[[FITTrainingFileMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumWeatherConditions:
            [self.fitWeatherConditionsMesgDelegate onWeatherConditionsMesg:[[FITWeatherConditionsMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumWeatherAlert:
            [self.fitWeatherAlertMesgDelegate onWeatherAlertMesg:[[FITWeatherAlertMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumGpsMetadata:
            [self.fitGpsMetadataMesgDelegate onGpsMetadataMesg:[[FITGpsMetadataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumCameraEvent:
            [self.fitCameraEventMesgDelegate onCameraEventMesg:[[FITCameraEventMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumGyroscopeData:
            [self.fitGyroscopeDataMesgDelegate onGyroscopeDataMesg:[[FITGyroscopeDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumAccelerometerData:
            [self.fitAccelerometerDataMesgDelegate onAccelerometerDataMesg:[[FITAccelerometerDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumMagnetometerData:
            [self.fitMagnetometerDataMesgDelegate onMagnetometerDataMesg:[[FITMagnetometerDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumBarometerData:
            [self.fitBarometerDataMesgDelegate onBarometerDataMesg:[[FITBarometerDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumThreeDSensorCalibration:
            [self.fitThreeDSensorCalibrationMesgDelegate onThreeDSensorCalibrationMesg:[[FITThreeDSensorCalibrationMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumOneDSensorCalibration:
            [self.fitOneDSensorCalibrationMesgDelegate onOneDSensorCalibrationMesg:[[FITOneDSensorCalibrationMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumVideoFrame:
            [self.fitVideoFrameMesgDelegate onVideoFrameMesg:[[FITVideoFrameMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumObdiiData:
            [self.fitObdiiDataMesgDelegate onObdiiDataMesg:[[FITObdiiDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumNmeaSentence:
            [self.fitNmeaSentenceMesgDelegate onNmeaSentenceMesg:[[FITNmeaSentenceMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumAviationAttitude:
            [self.fitAviationAttitudeMesgDelegate onAviationAttitudeMesg:[[FITAviationAttitudeMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumVideo:
            [self.fitVideoMesgDelegate onVideoMesg:[[FITVideoMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumVideoTitle:
            [self.fitVideoTitleMesgDelegate onVideoTitleMesg:[[FITVideoTitleMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumVideoDescription:
            [self.fitVideoDescriptionMesgDelegate onVideoDescriptionMesg:[[FITVideoDescriptionMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumVideoClip:
            [self.fitVideoClipMesgDelegate onVideoClipMesg:[[FITVideoClipMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSet:
            [self.fitSetMesgDelegate onSetMesg:[[FITSetMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumJump:
            [self.fitJumpMesgDelegate onJumpMesg:[[FITJumpMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSplit:
            [self.fitSplitMesgDelegate onSplitMesg:[[FITSplitMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSplitSummary:
            [self.fitSplitSummaryMesgDelegate onSplitSummaryMesg:[[FITSplitSummaryMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumClimbPro:
            [self.fitClimbProMesgDelegate onClimbProMesg:[[FITClimbProMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumFieldDescription:
            [self.fitFieldDescriptionMesgDelegate onFieldDescriptionMesg:[[FITFieldDescriptionMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumDeveloperDataId:
            [self.fitDeveloperDataIdMesgDelegate onDeveloperDataIdMesg:[[FITDeveloperDataIdMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumCourse:
            [self.fitCourseMesgDelegate onCourseMesg:[[FITCourseMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumCoursePoint:
            [self.fitCoursePointMesgDelegate onCoursePointMesg:[[FITCoursePointMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSegmentId:
            [self.fitSegmentIdMesgDelegate onSegmentIdMesg:[[FITSegmentIdMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSegmentLeaderboardEntry:
            [self.fitSegmentLeaderboardEntryMesgDelegate onSegmentLeaderboardEntryMesg:[[FITSegmentLeaderboardEntryMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSegmentPoint:
            [self.fitSegmentPointMesgDelegate onSegmentPointMesg:[[FITSegmentPointMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSegmentLap:
            [self.fitSegmentLapMesgDelegate onSegmentLapMesg:[[FITSegmentLapMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSegmentFile:
            [self.fitSegmentFileMesgDelegate onSegmentFileMesg:[[FITSegmentFileMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumWorkout:
            [self.fitWorkoutMesgDelegate onWorkoutMesg:[[FITWorkoutMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumWorkoutSession:
            [self.fitWorkoutSessionMesgDelegate onWorkoutSessionMesg:[[FITWorkoutSessionMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumWorkoutStep:
            [self.fitWorkoutStepMesgDelegate onWorkoutStepMesg:[[FITWorkoutStepMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumExerciseTitle:
            [self.fitExerciseTitleMesgDelegate onExerciseTitleMesg:[[FITExerciseTitleMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSchedule:
            [self.fitScheduleMesgDelegate onScheduleMesg:[[FITScheduleMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumTotals:
            [self.fitTotalsMesgDelegate onTotalsMesg:[[FITTotalsMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumWeightScale:
            [self.fitWeightScaleMesgDelegate onWeightScaleMesg:[[FITWeightScaleMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumBloodPressure:
            [self.fitBloodPressureMesgDelegate onBloodPressureMesg:[[FITBloodPressureMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumMonitoringInfo:
            [self.fitMonitoringInfoMesgDelegate onMonitoringInfoMesg:[[FITMonitoringInfoMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumMonitoring:
            [self.fitMonitoringMesgDelegate onMonitoringMesg:[[FITMonitoringMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumMonitoringHrData:
            [self.fitMonitoringHrDataMesgDelegate onMonitoringHrDataMesg:[[FITMonitoringHrDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSpo2Data:
            [self.fitSpo2DataMesgDelegate onSpo2DataMesg:[[FITSpo2DataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHr:
            [self.fitHrMesgDelegate onHrMesg:[[FITHrMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumStressLevel:
            [self.fitStressLevelMesgDelegate onStressLevelMesg:[[FITStressLevelMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumMaxMetData:
            [self.fitMaxMetDataMesgDelegate onMaxMetDataMesg:[[FITMaxMetDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHsaBodyBatteryData:
            [self.fitHsaBodyBatteryDataMesgDelegate onHsaBodyBatteryDataMesg:[[FITHsaBodyBatteryDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHsaEvent:
            [self.fitHsaEventMesgDelegate onHsaEventMesg:[[FITHsaEventMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHsaAccelerometerData:
            [self.fitHsaAccelerometerDataMesgDelegate onHsaAccelerometerDataMesg:[[FITHsaAccelerometerDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHsaGyroscopeData:
            [self.fitHsaGyroscopeDataMesgDelegate onHsaGyroscopeDataMesg:[[FITHsaGyroscopeDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHsaStepData:
            [self.fitHsaStepDataMesgDelegate onHsaStepDataMesg:[[FITHsaStepDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHsaSpo2Data:
            [self.fitHsaSpo2DataMesgDelegate onHsaSpo2DataMesg:[[FITHsaSpo2DataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHsaStressData:
            [self.fitHsaStressDataMesgDelegate onHsaStressDataMesg:[[FITHsaStressDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHsaRespirationData:
            [self.fitHsaRespirationDataMesgDelegate onHsaRespirationDataMesg:[[FITHsaRespirationDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHsaHeartRateData:
            [self.fitHsaHeartRateDataMesgDelegate onHsaHeartRateDataMesg:[[FITHsaHeartRateDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHsaConfigurationData:
            [self.fitHsaConfigurationDataMesgDelegate onHsaConfigurationDataMesg:[[FITHsaConfigurationDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHsaWristTemperatureData:
            [self.fitHsaWristTemperatureDataMesgDelegate onHsaWristTemperatureDataMesg:[[FITHsaWristTemperatureDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumMemoGlob:
            [self.fitMemoGlobMesgDelegate onMemoGlobMesg:[[FITMemoGlobMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSleepLevel:
            [self.fitSleepLevelMesgDelegate onSleepLevelMesg:[[FITSleepLevelMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumAntChannelId:
            [self.fitAntChannelIdMesgDelegate onAntChannelIdMesg:[[FITAntChannelIdMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumAntRx:
            [self.fitAntRxMesgDelegate onAntRxMesg:[[FITAntRxMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumAntTx:
            [self.fitAntTxMesgDelegate onAntTxMesg:[[FITAntTxMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumExdScreenConfiguration:
            [self.fitExdScreenConfigurationMesgDelegate onExdScreenConfigurationMesg:[[FITExdScreenConfigurationMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumExdDataFieldConfiguration:
            [self.fitExdDataFieldConfigurationMesgDelegate onExdDataFieldConfigurationMesg:[[FITExdDataFieldConfigurationMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumExdDataConceptConfiguration:
            [self.fitExdDataConceptConfigurationMesgDelegate onExdDataConceptConfigurationMesg:[[FITExdDataConceptConfigurationMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumDiveSummary:
            [self.fitDiveSummaryMesgDelegate onDiveSummaryMesg:[[FITDiveSummaryMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumAadAccelFeatures:
            [self.fitAadAccelFeaturesMesgDelegate onAadAccelFeaturesMesg:[[FITAadAccelFeaturesMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHrv:
            [self.fitHrvMesgDelegate onHrvMesg:[[FITHrvMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumBeatIntervals:
            [self.fitBeatIntervalsMesgDelegate onBeatIntervalsMesg:[[FITBeatIntervalsMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHrvStatusSummary:
            [self.fitHrvStatusSummaryMesgDelegate onHrvStatusSummaryMesg:[[FITHrvStatusSummaryMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumHrvValue:
            [self.fitHrvValueMesgDelegate onHrvValueMesg:[[FITHrvValueMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumRawBbi:
            [self.fitRawBbiMesgDelegate onRawBbiMesg:[[FITRawBbiMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumRespirationRate:
            [self.fitRespirationRateMesgDelegate onRespirationRateMesg:[[FITRespirationRateMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumChronoShotSession:
            [self.fitChronoShotSessionMesgDelegate onChronoShotSessionMesg:[[FITChronoShotSessionMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumChronoShotData:
            [self.fitChronoShotDataMesgDelegate onChronoShotDataMesg:[[FITChronoShotDataMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumTankUpdate:
            [self.fitTankUpdateMesgDelegate onTankUpdateMesg:[[FITTankUpdateMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumTankSummary:
            [self.fitTankSummaryMesgDelegate onTankSummaryMesg:[[FITTankSummaryMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSleepAssessment:
            [self.fitSleepAssessmentMesgDelegate onSleepAssessmentMesg:[[FITSleepAssessmentMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumSkinTempOvernight:
            [self.fitSkinTempOvernightMesgDelegate onSkinTempOvernightMesg:[[FITSkinTempOvernightMesg alloc] initWithMessage:message]];
            break;
        case FITMesgNumPad:
            [self.fitPadMesgDelegate onPadMesg:[[FITPadMesg alloc] initWithMessage:message]];
            break;

        default:
            break;
    }
}

@end
