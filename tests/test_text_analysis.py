from ai_media_lab.common.text_analysis import analyze_lecture_text, clean_transcript, segment_text


LECTURE_TEXT = """
Retrieval augmented generation connects a language model to trusted source material.
The retrieval step finds relevant passages before the model writes an answer.
Grounding matters because unsupported answers are hard to verify.
Chunking, embeddings, ranking, and citation quality all change the final result.
The best systems evaluate answers against the source documents and make failures visible.
"""


def test_lecture_analysis_contains_notes_quiz_and_study_guide():
    analysis = analyze_lecture_text(LECTURE_TEXT, topic="Retrieval Augmented Generation")

    assert analysis.title == "Retrieval Augmented Generation"
    assert "Executive Summary" in analysis.clean_notes
    assert len(analysis.key_concepts) >= 4
    assert len(analysis.quiz_questions) >= 4
    assert analysis.study_guide.flashcards


def test_clean_transcript_normalizes_spacing():
    assert clean_transcript(" hello   world  ! ") == "hello world!"


def test_segment_text_creates_monotonic_segments():
    segments = segment_text(LECTURE_TEXT)

    assert segments
    assert all(segment.end > segment.start for segment in segments)
    assert segments == sorted(segments, key=lambda segment: segment.start)

