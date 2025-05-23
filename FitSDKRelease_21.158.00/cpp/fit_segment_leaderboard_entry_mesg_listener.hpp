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


#if !defined(FIT_SEGMENT_LEADERBOARD_ENTRY_MESG_LISTENER_HPP)
#define FIT_SEGMENT_LEADERBOARD_ENTRY_MESG_LISTENER_HPP

#include "fit_segment_leaderboard_entry_mesg.hpp"

namespace fit
{

class SegmentLeaderboardEntryMesgListener
{
public:
    virtual ~SegmentLeaderboardEntryMesgListener() {}
    virtual void OnMesg(SegmentLeaderboardEntryMesg& mesg) = 0;
};

} // namespace fit

#endif // !defined(FIT_SEGMENT_LEADERBOARD_ENTRY_MESG_LISTENER_HPP)
